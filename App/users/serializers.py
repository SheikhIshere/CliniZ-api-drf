"""
users/serializers.py
"""

# core imports
from rest_framework import serializers

# validate password
from django.contrib.auth.password_validation import validate_password

# user
from .models import User

# Import authenticate to verify email and password
from django.contrib.auth import authenticate

# from model
from .models import Otp

# import timezone
from django.utils import timezone

# import timedelta
from datetime import timedelta

# generate otp
from .utils import generate_otp

# settings
from django.conf import settings

# send mail
from django.core.mail import send_mail


"""
User list serializer
"""
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



"""
User registration serializer
"""
class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True) 
    # full name = will be adding this after creating patient profile section
    password = serializers.CharField(required=True, write_only=True) 
    password2 = serializers.CharField(required=True, write_only=True)    

    def validate(self, attrs):
        # checking email
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                "error":"Email already exists."
            })
        
        # checking password
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "error":"Passwords do not match."
            })
        validate_password(attrs['password'])
        return attrs
    
    def create(self, validated_data):
        # popping password
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        # creating user
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        return user


"""
Account activation serializer
"""
class ActivatingAccountSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        given_otp = attrs.get("otp")
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None:
            raise serializers.ValidationError({"error": "Authentication required."})

        # get most recent active otp for the user (so we can increment attempts on wrong input)
        otp_obj = Otp.objects.filter(user=user, is_expired=False).order_by("-created_at").first()
        if not otp_obj:
            raise serializers.ValidationError({"error": "Invalid otp."})

        now = timezone.now()
        if otp_obj.created_at + timezone.timedelta(minutes=5) < now:
            otp_obj.is_expired = True
            otp_obj.save()
            raise serializers.ValidationError({"error": "Otp is expired."})

        # wrong OTP -> increment attempt and possibly expire
        if otp_obj.otp != given_otp:
            otp_obj.attempt += 1
            if otp_obj.attempt >= 3:
                otp_obj.is_expired = True
                # do NOT delete the user here — prefer locking or notifying
            otp_obj.save()
            if otp_obj.is_expired:
                raise serializers.ValidationError({"error": "Otp input reached its limit."})
            raise serializers.ValidationError({"error": "Invalid otp."})

        # correct OTP: save its id so create() can use the same instance (avoid race conditions)
        attrs["_otp_pk"] = otp_obj.pk
        return attrs

    def create(self, validated_data):
        otp_pk = validated_data.pop("_otp_pk", None)
        user = self.context.get("request").user

        otp = Otp.objects.filter(pk=otp_pk, user=user).first()
        if not otp:
            raise serializers.ValidationError({"error": "Otp not found."})

        # activate user and expire otp
        user = otp.user
        user.is_verified = True
        user.save()

        otp.is_expired = True
        otp.save()
        return user



"""
Login serializer
"""
class LoginSerializer(serializers.Serializer):
    # global
    _user: User = None

    # fields
    email = serializers.EmailField(required=True) 
    password = serializers.CharField(required=True, write_only=True)    

    def validate(self, attrs):
        # getting email and password value
        email = attrs.get('email')
        password = attrs.get('password')
        
        # checking email and password
        self._user = user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        # what if user not found
        if not user:
            raise serializers.ValidationError({
                "error":"Invalid email or password."
            })
        
        # deleting account if it is not verified
        if not user.is_verified:
            user.delete()
            raise serializers.ValidationError({
                "error":"Account is not verified."
            })

        return attrs
    
    def create(self, validated_data):
        return self._user


class LoginOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, max_length=6)

    def validate(self, attrs):
        req = self.context['request']
        _user = req.user
        try: 
            user = User.objects.get(email=_user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found."})
        given_otp = attrs['otp']

        otp_obj = Otp.objects.filter(user=user, otp=given_otp, is_expired=False).first()

        if not otp_obj:
            raise serializers.ValidationError({"error": "Invalid OTP."})

        if not user.is_verified:
            raise serializers.ValidationError({"error": "Account is not verified."})

        if otp_obj.created_at + timezone.timedelta(minutes=5) < timezone.now():
            otp_obj.is_expired = True
            otp_obj.save()
            Otp.objects.filter(user=user, is_expired=False).update(is_expired=True)
            raise serializers.ValidationError({"error": "OTP is expired."})

        # success path
        otp_obj.is_expired = True
        otp_obj.save()

        return attrs

    def create(self, validated_data):
        return self.context['request'].user


"""
Forget password serializer
using this as a forget password request resend email
for password reset
"""
class ForgetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        what if i use
        hacker will start doing putting mail 
        address in order to get my admin panel email
        or any sensitive email
        """
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        try:
            user = User.objects.get(email=email)
            reset_otp = generate_otp()
            # disabling previous OTPs for this user
            Otp.objects.filter(user=user, is_expired=False).update(is_expired=True)

            Otp.objects.create(
                user=user,
                otp=reset_otp,
            )

            # for debug only
            print('='*50)
            print(f"\nreset otp is: {reset_otp}\n")
            print('='*50)

            # sending otp throw mail
            subject = 'Forget Password OTP'
            message = f"Your OTP for password reset is: {reset_otp}.\nPlease use this OTP to reset your password. This OTP will expire in 10 minutes.\nIf you didn't request this, please ignore this email."
            email = email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )   
        
        except User.DoesNotExist:
            pass

        return validated_data


"""
verifying password resetting otp
"""

class PasswordResetVerifyOTPSerializer(serializers.Serializer):
    _user: User = None
    _otp: Otp = None

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            otp = attrs.get('otp')
            
            self._user = user = User.objects.get(email=attrs.get('email'))
            self._otp = reset_otp = Otp.objects.get(user=user, otp=otp, is_expired=False)
            
            if reset_otp:
                reset_otp.is_expired = True
                reset_otp.save()
            else:
                raise serializers.ValidationError({
                    "error":"Invalid otp."
                })
            
            # getting current time
            current_time = timezone.now()
            
            if reset_otp.created_at + timezone.timedelta(minutes=5) < current_time:
                raise serializers.ValidationError({
                    "error":"Otp is expired."
                })
            

        except (User.DoesNotExist, Otp.DoesNotExist):
            raise serializers.ValidationError({
                "error":"Invalid otp. or Email not found."
            })
        
        return attrs

    
    def create(self, validated_data):
        return self._user


"""
password reset - verify OTP serializer
"""
class PasswordResetConfirmSerializer(serializers.Serializer):

    _user: User = None
    _otp: Otp = None

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True) 

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
                
        try:            
            self._user = user = User.objects.get(email=email)
            self._otp = otp_obj = Otp.objects.filter(
                user=user,
                otp=otp,
                is_expired=False
            ).first()

            # FIX: Guard before accessing created_at
            if not otp_obj:
                raise serializers.ValidationError({
                    "error": "Invalid or expired OTP."
                })

            # Now safe to use created_at
            current_time = timezone.now()
            expiry_time = otp_obj.created_at + timedelta(minutes=10)

            if current_time > expiry_time:
                otp_obj.is_expired = True
                otp_obj.save()
                raise serializers.ValidationError({
                    "error": "Otp is expired. Please request a new otp."
                })

            if user.check_password(new_password):
                raise serializers.ValidationError({
                    "error": "New password cannot be the same as the current password."
                })
            
            if new_password != confirm_password:
                raise serializers.ValidationError({
                    "error": "New password and confirm password must match."
                })

            validate_password(new_password)

        except User.DoesNotExist:
            raise serializers.ValidationError({
                "error": "Invalid request."
            })
        
        return attrs
    
    def create(self, validated_data):
        # Set new password
        self._user.set_password(validated_data.get('new_password'))
        self._user.save()

        # Expire the verified OTP safely
        if self._otp:
            self._otp.is_expired = True
            self._otp.save()

        # Expire all other active OTPs for this user
        Otp.objects.filter(user=self._user, is_expired=False).update(is_expired=True)

        return self._user



"""
password Change serializer
"""
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # getting all of the data that user provided
        request = self.context.get('request')
        user = request.user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                "error":"Invalid old password."
            })
        
        if old_password == new_password:
            raise serializers.ValidationError({
                "error":"New password cannot be same as old password."
            })
        
        if new_password != confirm_password:
            raise serializers.ValidationError({
                "error":"New password and confirm password must match."
            })
        
        validate_password(new_password)
        
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data.get('new_password'))
        user.save()

        return user
