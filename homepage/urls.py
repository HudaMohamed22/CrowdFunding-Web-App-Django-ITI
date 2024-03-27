from django.urls import path
from homepage.views import landing, search


urlpatterns = [
    path('', landing, name="home.landing"),
    path('search/', search, name="search"),
]