from django.shortcuts import render
from homepage.forms import SearchForm
from project.models import Project, Tag

# Create your views here.

def landing(request):
    return render(request, "homepage/homepage.html")


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
