from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from helpers.decorators import authnoaccess
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .utils import generatetoken
from django.core.mail import EmailMessage
from django.conf import settings
import threading

'''class emailthread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()'''


def sendactivemail(user, request):
    currentsite = get_current_site(request)
    emailsub = 'Tasks Activation Link'
    emailbody = render_to_string('authenticate/activate.html', {
        'user': user,
        'domain': currentsite,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generatetoken.make_token(user)
    })

    email= EmailMessage(subject=emailsub, body=emailbody, from_email=settings.EMAIL_HOST_USER,
                 to=[user.email]
                 )
    email.send()



@authnoaccess
def register(request):
    if request.method == 'POST':

        context={'haserror': False, 'data':request.POST}

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        special = []

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password length must be greater than 6')
            context['haserror'] = True
        
        if not password.isalnum():
             messages.add_message(request, messages.ERROR, 'Passwords should have a mix of numbers, uppercase and lowercase characters')
             context['haserror'] = True

        if password.islower() or password.isupper() or password.isdigit():
            messages.add_message(request, messages.ERROR, 'Passwords should have a mix of numbers, uppercase and lowercase characters')
            context['haserror'] = True
            

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords are not similar')
            context['haserror'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR, 'Enter a valid email address')
            context['haserror'] = True

        if not username:
            messages.add_message(request, messages.ERROR, 'Provide a username')
            context['haserror'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username already exists. Please choose a different one')
            context['haserror'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email already exists. Please choose a different one')
            context['haserror'] = True

        if context['haserror']:
            return render(request, 'authenticate/register.html', context)
        
        user=User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        
        
        sendactivemail(user, request)

        messages.add_message(request, messages.SUCCESS, 'Account created successfully. Check your email to activate your account.')

        return redirect('login')


        




    return render(request, 'authenticate/register.html')


@authnoaccess
def logon(request):
    context={'data': request.POST}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if not user.isemailverified:
            messages.add_message(request, messages.ERROR, 'Email not verified. Please check your inbox')
            return render(request, 'authenticate/login.html', context)

        if not user:
            messages.add_message(request, messages.ERROR, 'invalid credentials')
            return render(request, 'authenticate/login.html', context)
        

        login(request, user)

        messages.add_message(request, messages.SUCCESS, f'Login successful. Welcome, {user.username}')

        return redirect(reverse('index'))


    return render(request, 'authenticate/login.html')

def logoutuser(request):
    logout(request)

    messages.add_message(request, messages.SUCCESS, 'Successfully logged out')

    return redirect(reverse('login'))

def activateuser(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))

        user=User.objects.get(pk=uid)

    except Exception as e:
        user=None

    if user and generatetoken.check_token(user, token):
        user.isemailverified = True
        user.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, you can now login')
        return redirect(reverse('login'))
    
    return render(request, 'authenticate/activatefailed.html',{'user': user})



# Create your views here.
