import re
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django import forms
from django.forms import ClearableFileInput
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class RegisterModelForm(UserCreationForm):
    class Meta:
        model  = CustomUser
        fields= ['username','first_name', 'last_name', 'password1','password2','mobile_phone','profile_picture']

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


COUNTRY_CHOICES = [
    ('None', 'Select Country'),  
    ('EG', 'Egypt'),
    ('US', 'United States'),
    ('UK', 'United Kingdom'),
]

class UserProfileForm(forms.ModelForm):
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'mobile_phone', 'profile_picture', 'birthdate', 'facebook_profile', 'country']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def validate_facebook_url(self, value):
        # regex to match Facebook URLs
        facebook_url_regex = r'^https?://(www\.)?facebook\.com/.+'
        
        if value and not re.match(facebook_url_regex, value):
            return False
        return True

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
    
    def clean_birthdate(self):
            birthdate = self.cleaned_data.get('birthdate')
            if birthdate:
                today = date.today()
                # check if birthdate is after today's date
                if birthdate > today:
                    raise forms.ValidationError("Birthdate cannot be in the future.")
            return birthdate
    
    def clean_facebook_profile(self):
        facebook_profile = self.cleaned_data.get('facebook_profile')
        if facebook_profile:
            if not self.validate_facebook_url(facebook_profile):
                raise ValidationError('Invalid Facebook URL')
        return facebook_profile

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return new_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password