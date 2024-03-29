from django.shortcuts import render,get_object_or_404
from homepage.forms import SearchForm
from project.models import Project, Tag,Category

# Create your views here.

def landing(request):
    latest_featured_projects = Project.objects.filter(is_featured=True).order_by('-featured_at')[:5]
    latest_created_projects = Project.objects.order_by('-created_at')[:5]
    return render(request, "homepage/homepage.html", {
        'latest_featured_projects': latest_featured_projects,
        'latest_created_projects': latest_created_projects
    })


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


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'homepage/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = Project.objects.filter(category_id=category_id)
    return render(request, 'homepage/category_detail.html', {'category': category, 'projects': projects})
