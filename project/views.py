from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from project.models import Project,Picture
from project.forms import Project_ModelForm

# Create your views here.
def base_page(request):
    return HttpResponse("hiiiiiiiiiiiiiiiii")


def createProject(request):
    form = Project_ModelForm()
    if request.method == 'POST':
        form = Project_ModelForm(request.POST, request.FILES)
        if form.is_valid():
            
            return HttpResponse("hkhgjhvj")

    return render(request, 'project/create-project.html',
                  context={"form":form})