# authentication
from django.contrib.auth import authenticate, logout, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# core rest
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

# serializers
from .serializers import (
    PatientSerializer, 
    RegistrationsSerializer,
    UserLoginSerializer
)

# redirecting
from django.shortcuts import redirect

# user models
from django.contrib.auth.models import User
from .models import Patient

# for sending email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

# status code
from rest_framework import status


# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationsSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/patient/activate/{uid}/{token}"

            # just for debugging only
            print(f"username: {user.username} and passwod: {user.password}")
            print(f"token: {token}")
            print(f"uid: {uid}")

            # send email
            name = f"{user.first_name} {user.last_name}"
            email_subject = "Activate your account"
            email_body = render_to_string(
                "sending_mail/confirm_email.html",
                {
                    'confirm_link': confirm_link,
                    'name': name,
                },
            )

            email = EmailMultiAlternatives(
                email_subject,
                '',
                to=[user.email],
            )
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response('Check your email for confirmation')
        
        return Response(serializer.errors)


def activating_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('registration') # chenge to desired page

    else:
        return redirect('registration')



class UserLogInApiView(APIView):    
    serializer_class = UserLoginSerializer
    def post(self, request):
        # serializer_class = RegistrationsSerializer
        serializer = self.serializer_class(data=self.request.data)
        # checking if user is authenticated or not
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                print(f"got_token: {token}")
                print(f"another _ {_}")
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': 'Invalid credentials'})

        return Response(serializer.errors)

class UserLogOutApiView(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)