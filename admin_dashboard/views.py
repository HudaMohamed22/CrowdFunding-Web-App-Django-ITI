from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from project.forms import Category_ModelForm
from project.models import Category, Project
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import admin_required

# Create your views here.

@login_required(login_url='login')
@admin_required
def landing(request):
    return render(request, "admin_dashboard/dashboard.html")

@login_required(login_url='login')
@admin_required
def create_new_category(request):
    form = Category_ModelForm()
    if request.method == 'POST':
        form = Category_ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'admin_dashboard/dashboard.html')
    return render(request, 'admin_dashboard/create_category.html', context={"categoryForm": form})


@login_required(login_url='login')
@admin_required
def edit_specific_category(request, category_id):
    selected_category = Category.get_category_by_id(category_id)
    form = Category_ModelForm(instance=selected_category)
    if request.method == 'POST':
        form = Category_ModelForm(request.POST, instance=selected_category)
        if form.is_valid():
            form.save()
            return redirect('all_categories')
    return render(request, 'admin_dashboard/edit_category.html', context={"categoryForm": form})


@login_required(login_url='login')
@admin_required
def delete_specific_category(request, category_id):
    deleted_category = Category.objects.get(id=category_id)
    deleted_category.delete()
    url = reverse('all_categories')
    return redirect(url)


@login_required(login_url='login')
@admin_required
def mark_featured(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        is_featured = request.POST.get('is_featured')
        try:
            project = Project.objects.get(pk=project_id)
            project.is_featured = is_featured == 'on'
            if project.is_featured:
                project.featured_at = timezone.now()  # set featured_at to current date and time
            project.save()
            return redirect('all_projects')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return redirect('all_projects')

def page_403(request):
    return render(request, "403.html")