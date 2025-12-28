from django.shortcuts import redirect

def redirect_script(request):
    return redirect('swagger-ui')