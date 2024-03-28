from django.shortcuts import redirect, render, reverse,get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from project.forms import Project_ModelForm,ProjectReport_ModelForm
from django.contrib.auth.decorators import login_required
from project.models import Project,Picture,Tag,Comment,Project_Report,Comment_Report
from users.models import CustomUser
from django.contrib import messages #import messages
import re



@login_required(login_url='login')
def createProject(request):
    form = Project_ModelForm()
    if request.method == 'POST':
        form = Project_ModelForm(request.POST, request.FILES)
        if form.is_valid():
            tag_objects = []
            # Handle new tags
            tags_input = request.POST.get("newTag", "")
            tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tag_objects.append(tag)
            
            # Handle existing tags           to get all tags not the last one only
            existing_tag_ids = request.POST.getlist("tag")
            if existing_tag_ids:
                for tag_id in existing_tag_ids:
                    try:
                        existing_tag = Tag.objects.get(id=tag_id)
                        tag_objects.append(existing_tag)
                    except Tag.DoesNotExist:
                        form.add_error('tag', "invalid tag")

         # ----------- user part handling and save -----------------------
            # Retrieve the actual user instance from the lazy object
            try:
                user_instance = CustomUser.objects.get(pk=request.user.pk)
                project = form.save(commit=False)
                project.owner = user_instance
                project.save()
                if tag_objects:
                    project.tag.set(tag_objects)   # to update the many-to-many relationship (overwrite)

            except ObjectDoesNotExist:
                    # print("hereeeeeeeeeeeeeee")
                    url = reverse("login")
                    return redirect(url)  

             
            # ----------- image part handling-----------------------
            project_images = request.FILES.getlist('images')
            for img in project_images:
                Picture.objects.create(project=project, image=img)

           #----------------------- submit and redirect
            messages.success(request, "Message sent." )
            url = reverse("home.landing")
            return redirect(url)  

    return render(request, 'project/create-project.html', context={"form":form})

@login_required(login_url='login')
def cancelProject(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user_instance = get_object_or_404(CustomUser,pk=request.user.pk)

        if project.owner !=user_instance:
            return HttpResponse("You are not authorized to delete this project.")
    
        donation = project.current_donation
        total_target = project.total_target
            
        if donation < total_target*.25:
            project.delete()

            url = reverse("home.landing")
            return redirect(url)  
        else:
            return HttpResponse("Can't Delete This Project Because the Donations Amount Exceed 25'%' of the Total Target")
        
@login_required(login_url='login')        
def create_ProjectReport(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    user_instance = get_object_or_404(CustomUser,pk=request.user.pk)

    if request.method == "POST":
         form = ProjectReport_ModelForm(request.POST, request.FILES)
         if form.is_valid() and not is_spam(user_instance.pk,project_id):
                report = form.save(commit=False)
                report.user = user_instance
                report.project=project
                report.save()
           
    url = reverse("show", kwargs={'project_id': project_id})
    return redirect(url)       

def is_spam(user_id, project_id):
    return (Project_Report.objects.filter(user=user_id, project=project_id).count() > 3)





@login_required(login_url='login')        
def create_commentReport(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user_instance = get_object_or_404(CustomUser,pk=request.user.pk)
    project = comment.project

    if (not is_spam_comment(user_instance.pk,comment.pk)):
        Comment_Report.objects.create(
                    comment=comment,
                    user=user_instance
                )
    if comment.Comment_Reports.all().count() > 10: 
        comment.delete()
    url = reverse("show", kwargs={'project_id': project.pk})
    return redirect(url)  

def is_spam_comment(user_id, comment_id):
    return (Comment_Report.objects.filter(user=user_id, comment=comment_id).count() >= 3)

# just for test 
def showProjectDetails(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user_instance = get_object_or_404(CustomUser,pk=request.user.pk)
        comments = project.comments.all()
        target_threshold = project.total_target*.25
        report_project_Form = ProjectReport_ModelForm()
        return render(request, "project/project_datails_test.html",
                    context={"project": project,"currentUser":user_instance,'target_threshold': target_threshold,
                            "report_project_Form":report_project_Form ,"comments":comments})
 