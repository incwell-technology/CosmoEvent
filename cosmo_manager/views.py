from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def verified_user_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))
    return render(request, "cosmo_manager/verified-view.html")

def not_verified_index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))
        
    return render(request, "cosmo_manager/not-verified-view.html")
