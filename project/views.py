from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.shortcuts import redirect, render, reverse,get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from project.forms import  Project_ModelForm
from django.contrib.auth.decorators import login_required
from project.models import Donation, Project,Picture,Tag,Comment
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
def project_details(request, id):
    project = get_object_or_404(Project, id=id)
    tags = project.tag.all()
    rate=int(project.rate) #tet3adel hayeb2a esmha avg rating
    image_urls = project.get_image_urls()
    comments= project.comments.all()
    counter = list(range(len(image_urls)))
    context = {
        'project': project,
        'tags': tags,
        'image_urls': image_urls,
        'counter': counter,
        "rate": rate,
        "comments": comments
  
    }

    return render(request, "project/project_details.html", context)

#mehtagen net2aked el far2 benhom 
@login_required(login_url='login')

def create_comment(request, project_id):
    if not request.user.is_authenticated :
        return redirect('login')  
    else:
        user = CustomUser.objects.get(pk=request.user.pk)
        project = Project.objects.get(pk=project_id)
        if request.method == 'POST':
            comment_text = request.POST.get('comment', '')
            if comment_text.strip():
                comment = Comment.objects.create(
                    comment=comment_text,
                    project=project,
                    user=user
                )
                return redirect('project_details', project_id)

        return render(request, "project/project_details.html", context={"user": user, "project": project})





def showProjectDetails(request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        user_instance = get_object_or_404(CustomUser,pk=request.user.pk)
        target_threshold = project.total_target*.25
        return render(request, "project/project_datails_test.html",
                    context={"project": project,"currentUser":user_instance,'target_threshold': target_threshold})
 