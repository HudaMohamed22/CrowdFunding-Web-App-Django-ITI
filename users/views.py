from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from users.forms import  RegisterModelForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


def activateEmail(request, user, to_email):
    mail_subject = "NileFund Account Activation."
    message = render_to_string("users/activation_email.html", {
        'user': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'Account created successfully. Please check your email to activate your account to be able to login.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        url = reverse('login')
        return redirect(url)
    else:
        return HttpResponse('Activation link is invalid or expired!')


def register_user(request):
    if request.user.is_authenticated:
        url = reverse('home.landing')
        return redirect(url)
    else:
        form = RegisterModelForm()
        if request.method=='POST':
            form = RegisterModelForm(request.POST,request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                # activation function call
                activateEmail(request, user, form.cleaned_data.get('username'))
        return render(request,
                    'users/register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        url = reverse('home.landing')
        return redirect(url)
    else:
        if request.method=='POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request,user)
                url = reverse('home.landing')
                return redirect(url)
            else:
                messages.error(request,'incorrect email or password')

        return render(request,'users/login.html')


def logout_user(request):
    logout(request)
    url = reverse('login')
    return redirect(url)
