from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from cosmo_user import models as cosmo_models
from django.contrib.auth import authenticate, login, logout


def verified_user_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    try:
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        if cosmo_user.verified:
            return render(request, "cosmo_manager/verified-view.html")
        else:
            return render(request, "cosmo_manager/not-verified-view.html")
    except cosmo_models.CosmoUser.DoesNotExist:
        logout(request)        
        return HttpResponseRedirect(reverse('user-login'))


def not_verified_index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    try:
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        if cosmo_user.verified:
            return render(request, "cosmo_manager/verified-view.html")
        else:
            return render(request, "cosmo_manager/not-verified-view.html")
    except cosmo_models.CosmoUser.DoesNotExist:
        logout(request)        
        return HttpResponseRedirect(reverse('user-login'))