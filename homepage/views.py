from django.shortcuts import render,get_object_or_404
from homepage.forms import SearchForm
from django.db.models import Avg, Count, F
from project.models import Project, Tag,Category
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

def get_highest_rated_running_projects():     
    running_projects = Project.objects.filter(end_date__gte=date.today(), current_donation__lt=F('total_target'))     
    highest_rated_running_projects = running_projects.annotate(avg_rate=Avg('rate')).order_by('-avg_rate')[:5]     
    return highest_rated_running_projects  


def landing(request):
    latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-featured_at')[:5]
    latest_created_projects = Project.objects.order_by('-created_at')[:5]
    highest_rated_projects = get_highest_rated_running_projects()    
    # highest_rated_projects = Project.objects.annotate(avg_rate=Avg('rate')).order_by('-avg_rate')[:5]
    categories = Category.get_all_categories()
    categories_with_projects_count = Category.objects.annotate(num_projects=Count('projects'))
    return render(request, "homepage/homepage.html", {
        'latest_featured_projects': latest_featured_projects,
        'latest_created_projects': latest_created_projects,
        'highest_rated_projects': highest_rated_projects,
        'categories_list': categories_with_projects_count
    })

def show_projects(request):
    projects = Project.objects.all()
    for project in projects: #subtraction process
        project.remaining_target = project.total_target - project.current_donation
    return render(request, "homepage/all_Projects.html", {'projects': projects})


def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        search_option = form.cleaned_data['search_option']
        query = form.cleaned_data['query']
        
        if search_option == 'project':
            results = Project.objects.filter(title__icontains=query)
        elif search_option == 'tag':
            try:
                tag = Tag.objects.get(name__iexact=query)
                results = tag.projects.all()
            except:
                results = []
        else:
            results = []
    else:
        results = []
    return render(request, 'homepage/search_results.html', {'searchForm': form, 'searchResults': results})


def show_categories(request):
    categories = Category.get_all_categories()
    return render(request, 'homepage/all_categories.html', {'categories': categories})

@login_required(login_url='login')
def category_projects(request, category_id):
    try:
        selected_category = Category.get_category_by_id(category_id)
        category_projects = Project.objects.filter(category_id=category_id)
        return render(request, 'homepage/category_projects.html', {'category_projects': category_projects, 'selected_category':selected_category})
    except Exception as e:
        return render(request,'404.html')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'homepage/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        projects = Project.objects.filter(category_id=category_id)
        return render(request, 'homepage/category_detail.html', {'category': category, 'projects': projects})
    except Exception as e:
        return render(request,'404.html')
