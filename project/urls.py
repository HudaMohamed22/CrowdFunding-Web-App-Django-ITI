
from django.urls import path
from project.views import createProject,showProjectDetails,cancelProject,create_ProjectReport,create_commentReport
from project import views
from project.views import createProject,showProjectDetails,cancelProject,rate_project
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('<int:id>', views.project_details, name='project_details'),
    path('<int:project_id>/comment', views.create_comment, name='create_comment'), 
    path('show/<int:project_id>',showProjectDetails,name='show'), #de mehtaga tetshal zzabteha  ya huda
    path('cancelProject/<int:project_id>',cancelProject,name='cancel_project'),
    path('<int:id>/rate', rate_project, name='rate_project'),
    path('createProjectReport/<int:project_id>',create_ProjectReport,name='create_ProjectReport'),
    path('create_CommentReport/<int:comment_id>',create_commentReport,name='create_commentReport')



    #path('<int:id>/test',test,name='test'),

]