
from django.urls import path
from project.views import createProject
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),

]