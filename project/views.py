from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from project.forms import  Project_ModelForm
from django.contrib.auth.decorators import login_required
from project.models import Donation, Project,Picture,Tag,Comment
from users.models import CustomUser


@login_required(login_url='login')
def createProject(request):
    form = Project_ModelForm()
    # print(type(request.user))  # Check the type of request.user, it should be LazyUser
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
            # print(existing_tag_ids,"tttttttttttttttttttttttttttttttttt")
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

                    # form.save_m2m()
                # print(type(project.tag),"yyyyyyyyyyyyyyyy")
                # print(project.tag,"mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

            except ObjectDoesNotExist:
                    # print("hereeeeeeeeeeeeeee")
                    url = reverse("login")
                    return redirect(url)  

             
            # ----------- image part handling-----------------------
            project_images = request.FILES.getlist('images')
            for img in project_images:
                Picture.objects.create(project=project, image=img)

            return HttpResponse("User: {}".format(user_instance))

    return render(request, 'project/create-project.html', context={"form":form})


# @login_required
# def create_project(request):
#     if request.method == 'POST':
#         form = ProjectFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.user = request.user
#             project.save()

#             files = request.FILES.getlist('file')
#             for f in files:
#                 Photo.objects.create(project=project, photo=f)

#             return redirect('project_list')
#     else:
#         form = ProjectFileForm()

#     return render(request, 'projects/project_form.html', {'form': form})



# def createProject(request):
#     form = Project_ModelForm()
#     print(type(request.user))  # Check the type of request.user, it should be LazyUser
#     # print('hhhhhhhhhhhhh')

#     if request.method == 'POST':
#         form = Project_ModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(type(request.POST['category']),"      ",request.POST['category'])
          
#             # ----------- tag part handling-----------------------

#             if "tag" in request.POST or request.POST['newTag']!="":
#                 tag_objects = []
#                 if(request.POST['newTag']!= ''):    
#                     tags_input = request.POST.get("newTag", "")
#                     tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

#                     for tag_name in tags_list:
#                         # Check if tag_name matches the regex pattern
#                         if not re.match(r'^[a-zA-Z0-9_]+$', tag_name):
#                            form.add_error('tag',"Please Enter valid Tag with letter,digits or underscore only ")

#                         tag, created = Tag.objects.get_or_create(name=tag_name)
#                         tag_objects.append(str(tag.id))
#                     print("listttttttt",tag_objects)
#                 if form.cleaned_data['tag']:
#                     tag_objects.append(request.POST['tag'])

#                 request.POST = request.POST.copy()
#                 request.POST.update({"tag": tag_objects})
#                 print("listttttttt222222222222222222222222222",tag_objects)

#             # ----------- user part handling and save -----------------------
#             # Retrieve the actual user instance from the lazy object
#             user_instance = CustomUser.objects.get(pk=request.user.pk)
#             project = form.save(commit=False)
#             project.owner = user_instance
#             project.save()  
#             form.save_m2m()  

#             # ----------- image part handling-----------------------
#             project_images = request.FILES.getlist('images')
#             for img in project_images:
#                 Picture.objects.create(project=project, image=img)

#             return HttpResponse("User: {}".format(user_instance))

#     return render(request, 'project/create-project.html', context={"form":form})



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


