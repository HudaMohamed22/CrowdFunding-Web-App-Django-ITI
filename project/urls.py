
from django.urls import path

from project.views import base_page
urlpatterns = [
    path('', base_page, name='project.base_page' ),
   

]