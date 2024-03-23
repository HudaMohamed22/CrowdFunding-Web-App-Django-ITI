from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse

# Create your views here.
def base_page(request):
    return HttpResponse("hiiiiiiiiiiiiiiiii")