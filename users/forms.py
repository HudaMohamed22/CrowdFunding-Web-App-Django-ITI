import re
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django import forms
from django.forms import ClearableFileInput

class RegisterModelForm(UserCreationForm):
    class Meta:
        model  = CustomUser
        fields= ['first_name', 'last_name', 'username', 'password1','password2','mobile_phone','profile_picture']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        errors = []

        if CustomUser.objects.filter(username=username).exists():
            errors.append("This email is already taken. Please choose a different one.")

        elif not re.match(r'^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$', username):
            errors.append("Please enter a valid email address.")

       
        if errors:
            self.add_error('username', errors)

        return username

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        errors = []
        if mobile_phone and not re.match(r'^01[0125][0-9]{8}$', mobile_phone):
            errors.append("Mobile phone number must be a valid Egyptian phone number.")
        
        if errors:
            self.add_error('mobile_phone', errors)
        
        return mobile_phone

    # def clean_profile_picture(self):
    #     profile_picture = self.cleaned_data['profile_picture']
    #     if profile_picture:
    #         if not profile_picture.endswith(('.jpg', '.jpeg', '.png')):
    #             raise ValidationError("Profile picture must be in JPG, JPEG, or PNG format.")
    #     return profile_picture
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            self.add_error('first_name', "First name must be at least 2 characters long.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2:
            self.add_error('last_name', "Last name must be at least 2 characters long.")
        return last_name


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_phone', 'profile_picture']
        widgets = {
            'profile_picture': ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if mobile_phone and not re.match(r'^01[0125][0-9]{8}$', mobile_phone):
            raise forms.ValidationError("Mobile phone number must be a valid Egyptian phone number.")
        return mobile_phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2:
            raise forms.ValidationError("Last name must be at least 2 characters long.")
        return last_name

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if not profile_picture:
            return 'users/images/default_profile_picture.jpg'  # set default picture path
        return profile_picture

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)