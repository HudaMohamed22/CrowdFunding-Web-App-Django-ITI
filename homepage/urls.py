from django.urls import path
from homepage.views import landing, search, category_list, category_detail, show_projects, show_categories, category_projects


urlpatterns = [
    path('', landing, name="home.landing"),
    path('search/', search, name="search"),
    path('categories/', category_list, name='category.list'),
    path('category/<int:category_id>/', category_detail, name='category.detail'),
    path('all_projects/', show_projects, name='all_projects'),
    path('all_categories/', show_categories, name='all_categories'),
    path('<int:category_id>', category_projects, name="category_projects"),
]