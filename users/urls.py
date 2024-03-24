from django.urls import path
from users.views import  register_user, login_user,logout_user, activate


urlpatterns = [
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]