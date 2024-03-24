from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class CustomUser(User):
    mobile_regex = RegexValidator(regex=r'^01[0125]{1}[0-9]{8}$', message="Enter a valid Egyptian phone number")
    mobile_phone = models.CharField(validators=[mobile_regex], max_length=11)
    profile_picture = models.ImageField(upload_to='users/images', blank=True, null=True, default='users/images/default_profile_picture.jpg')

    @property
    def profile_picture_url(self):
        return f'/media/{self.profile_picture}'
