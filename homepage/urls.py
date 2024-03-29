from django.urls import path
from homepage.views import landing, search, category_list, category_detail


urlpatterns = [
    path('', landing, name="home.landing"),
    path('search/', search, name="search"),
    path('categories/', category_list, name='category.list'),
    path('category/<int:category_id>/', category_detail, name='category.detail'),
]