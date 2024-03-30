from django.urls import path
from users.views import  register_user, login_user,logout_user, activate,change_password,edit_profile, view_profile,delete_account,view_projects,view_donations


urlpatterns = [
    path('login', login_user, name='login'),
    path('register', register_user, name='register'),
    path('logout', logout_user, name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile', view_profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit.profile'),
    path('change-password/', change_password, name='change.password'),
    path('delete-account/', delete_account, name='delete.account'),
    path('view-projects/', view_projects, name='view.projects'),
    path('view-donations/', view_donations, name='view.donations'),
]