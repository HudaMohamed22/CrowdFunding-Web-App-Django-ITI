
from django.urls import path
from project.views import createProject,cancelProject,create_ProjectReport,create_commentReport,rate_project
from project import views
urlpatterns = [
    path('createProject', createProject, name='project.create_project'),
    path('<int:id>', views.project_details, name='project_details'),
    path('<int:project_id>/comment', views.create_comment, name='create_comment'), 
    path('cancelProject/<int:project_id>',cancelProject,name='cancel_project'),
    path('<int:id>/rate', rate_project, name='rate_project'),
    path('createProjectReport/<int:project_id>',create_ProjectReport,name='create_ProjectReport'),
    path('create_CommentReport/<int:comment_id>',create_commentReport,name='create_commentReport'),
    path('<int:project_id>/donate', views.add_donations, name='add_donations'),


    #path('<int:id>/test',test,name='test'),

]