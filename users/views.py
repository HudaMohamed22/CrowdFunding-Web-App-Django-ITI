from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
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
from users.forms import UserProfileForm
from .forms import UserProfileForm, ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseServerError
from project.models import Project, Donation

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
    url = reverse('home.landing')
    return redirect(url)

def view_profile(request):
    try:
        if request.user.is_authenticated and not request.user.is_superuser:
            user = request.user
            context = {
                'user': user
            }
            return render(request, 'users/profile.html', context)
        else:
            # not authenticated? redirect to login
            return redirect('login')
    except Exception as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))
@login_required(login_url='login')    
def edit_profile(request):
    custom_user = request.user.customuser
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=custom_user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserProfileForm(instance=custom_user)
    return render(request, 'users/edit_profile.html', {'user_form': user_form})

@login_required(login_url='login')  
def change_password(request):
    try:
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = request.user
                current_password = form.cleaned_data['current_password']
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']
                
                # check if the current password is correct
                if user.check_password(current_password):
                    if new_password != current_password:
                        if new_password == confirm_password:
                            # set the new password and save the user
                            user.set_password(new_password)  
                            user.save()
                            update_session_auth_hash(request, user)
                            messages.success(request, 'Your password has been changed successfully.')
                            return redirect('profile')  
                        else:
                            messages.error(request, 'New password and confirm password do not match.')
                    else:
                        messages.error(request, 'New password cannot be the same as the current password.')
                else:
                    messages.error(request, 'Current password is incorrect.')
        else:
            form = ChangePasswordForm()
        return render(request, 'users/change_password.html', {'form': form})
    except Exception as e:
        return HttpResponseServerError("An error occurred: {}".format(str(e)))
    
@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            user.delete()
            return JsonResponse({'success': True, 'message': 'Your account has been successfully deleted.'})
        else:
            return JsonResponse({'success': False, 'message': 'Wrong password!'})

    # if the request method is not POST
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required(login_url='login')
def view_projects(request):
  
    user_projects = Project.objects.filter(owner=request.user)

    for project in user_projects: #subtraction process
        project.remaining_target = project.total_target - project.current_donation

    # pass the projects to the template context
    return render(request, 'users/view_projects.html', {'user_projects': user_projects})

@login_required(login_url='login')
def view_donations(request):
    user_donations = Donation.objects.filter(user=request.user)

    # pass the user's donations to the template context
    return render(request, 'users/view_donations.html', {'user_donations': user_donations})