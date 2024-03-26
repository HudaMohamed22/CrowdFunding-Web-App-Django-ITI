
from django.urls import path
from project.views import createProject,showProjectDetails,cancelProject
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('show/<int:project_id>',showProjectDetails,name='show'),
    path('cancelProject/<int:project_id>',cancelProject,name='cancel_project')

]