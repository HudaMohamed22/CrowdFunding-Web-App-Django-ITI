from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from users.forms import  RegisterModelForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_user(request):
    if request.user.is_authenticated:
        url = reverse('home.landing')
        return redirect(url)
    else:
        form = RegisterModelForm()
        if request.method=='POST':
            form = RegisterModelForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for ' + user)
                url = reverse('login')
                return redirect(url)
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
                messages.info(request,'incorrect email or password')

        return render(request,'users/login.html')


def logout_user(request):
    logout(request)
    url = reverse('login')
    return redirect(url)
