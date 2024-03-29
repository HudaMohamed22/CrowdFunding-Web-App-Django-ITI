from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from project.forms import Category_ModelForm
from project.models import Category, Project
from django.http import JsonResponse


# Create your views here.


def landing(request):
    return render(request, "admin_dashboard/dashboard.html")


def create_new_category(request):
    form = Category_ModelForm()
    if request.method == 'POST':
        form = Category_ModelForm(request.POST)
        if form.is_valid():
            form.save()
            # return JsonResponse({'success': True}) 
            return render(request, 'admin_dashboard/dashboard.html')
        # else:
        #     errors = form.errors.as_json()
        #     return JsonResponse({'success': False, 'errors': errors})
    # return render(request, 'admin_dashboard/dashboard.html', context={"categoryForm": form})
    return render(request, 'admin_dashboard/create_category.html', context={"categoryForm": form})



def show_categories(request):
    categories = Category.get_all_categories()
    return render(request, 'admin_dashboard/all_categories.html', {'categories': categories})


def edit_specific_category(request, category_id):
    selected_category = Category.get_category_by_id(category_id)
    form = Category_ModelForm(instance=selected_category)
    if request.method == 'POST':
        form = Category_ModelForm(request.POST, instance=selected_category)
        if form.is_valid():
            form.save()
            return redirect('all_categories')
    return render(request, 'admin_dashboard/edit_category.html', context={"categoryForm": form})



def delete_specific_category(request, category_id):
    deleted_category = Category.objects.get(id=category_id)
    deleted_category.delete()
    url = reverse('all_categories')
    return redirect(url)


def category_projects(request, category_id):
    selected_category = Category.get_category_by_id(category_id)
    category_projects = Project.objects.filter(category_id=category_id)
    # category_projects = Project.objects.filter(category_id=category_id, owner_id=request.user.id)
    return render(request, 'admin_dashboard/category_projects.html', {'category_projects': category_projects, 'selected_category':selected_category})

def show_projects(request):
    projects = Project.objects.all()
    return render(request, "admin_dashboard/all_Projects.html", {'projects': projects})


def mark_featured(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        is_featured = request.POST.get('is_featured')
        try:
            project = Project.objects.get(pk=project_id)
            project.is_featured = is_featured == 'on' 
            project.save()
            return redirect('all_projects') 
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 
    return redirect('all_projects')  