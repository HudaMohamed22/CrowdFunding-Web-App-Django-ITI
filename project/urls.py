
from django.urls import path
from project import views
from project.views import createProject
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('<int:id>', views.project_details, name='project_details'),
    path('<int:project_id>/comment', views.create_comment, name='create_comment'),
]