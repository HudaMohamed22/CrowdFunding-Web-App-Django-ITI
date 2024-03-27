from django.urls import path
from homepage.views import landing


urlpatterns = [
    path('', landing, name="home.landing"),
]