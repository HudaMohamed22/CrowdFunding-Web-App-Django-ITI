
from django.urls import path
from project import views
from project.views import createProject,showProjectDetails,cancelProject
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('<int:id>', views.project_details, name='project_details'),
    path('<int:project_id>/comment', views.create_comment, name='create_comment'), 
    path('show/<int:project_id>',showProjectDetails,name='show'), #de mehtaga tetshal zzabteha  ya huda
    path('cancelProject/<int:project_id>',cancelProject,name='cancel_project')

]