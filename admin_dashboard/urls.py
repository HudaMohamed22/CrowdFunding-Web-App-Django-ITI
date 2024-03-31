from django.urls import path
from admin_dashboard.views import landing, create_new_category, delete_specific_category, edit_specific_category, mark_featured


urlpatterns = [
    path('', landing, name='admin_dashboard'),
    # path('all_projects/', show_projects, name='all_projects'),
    # path('', create_new_category, name='admin_dashboard'),
    path('create_category/', create_new_category, name='create_category'),
    path('edit_category/', create_new_category, name='create_category'),
    path('delete/<int:category_id>', delete_specific_category, name="delete_category"),
    path('edit/<int:category_id>', edit_specific_category, name="edit_category"),
    path('mark_featured/', mark_featured, name='mark_featured'),
]