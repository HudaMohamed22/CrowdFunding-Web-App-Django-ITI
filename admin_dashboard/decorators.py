from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, reverse

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            # return HttpResponseForbidden("You are not authorized to access this page.")
            return redirect('forbidden_access')
        return function(request, *args, **kwargs)
    return wrap
