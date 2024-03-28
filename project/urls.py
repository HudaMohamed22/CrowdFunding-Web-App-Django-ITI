
from django.urls import path
from project.views import createProject,showProjectDetails,cancelProject,create_ProjectReport,create_commentReport
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('show/<int:project_id>',showProjectDetails,name='show'),
    path('cancelProject/<int:project_id>',cancelProject,name='cancel_project'),
    path('createProjectReport/<int:project_id>',create_ProjectReport,name='create_ProjectReport'),
    path('create_CommentReport/<int:comment_id>',create_commentReport,name='create_commentReport')


]