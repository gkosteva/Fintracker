from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is not in the correct format'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email is taken, please use another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username is taken'}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        contex = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password is too weak!")
                    return render(request, 'authentication/register.html', contex)

            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = False

            domain = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = "http://" + domain + link

            email_subject = 'Activate your account'
            email_body = 'Hi, ' + user.username + '! Please use this link to verify your account\n' + activate_url
            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email]
            )
            email.send(fail_silently=False)
            user.save()
            messages.success(request, "Register successfully!")
            print(request.POST)
            return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')
