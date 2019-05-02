from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cosmo_user import models as cosmo_models
from django.contrib import messages
from cosmo_user.common import register_user

def user_login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'cosmo_user/login.html', {'message': 'Login', 'title': 'Cosmo Event | Login'})
        else:
            return HttpResponseRedirect(reverse('user-index'))

    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'cosmo_user/login.html', {'message': 'Invalid Credentials'})
        else:
            login(request, user)
            cosmo_user = cosmo_models.CosmoUser.objects.get(user=user)
            if not cosmo_user.verified:
                return HttpResponseRedirect(reverse('not-verified-index'))
            return HttpResponseRedirect(reverse('user-index'))


def user_logout(request):
    if request.method == 'GET':
        print('logout get')
        return HttpResponseRedirect(reverse('user-index'))

    else:
        logout(request)
        print('logout post')
        return HttpResponseRedirect(reverse('user-login'))


def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-index'))
    if request.method == 'GET':
        return render(request, 'cosmo_user/register.html')

    if request.method == 'POST':
        if User.objects.filter(email=request.POST['email']).exists():
            messages.success(request, "User with this email alerady exists.", extra_tags="0")
            context = {}
            context.update({'first_name':request.POST['first_name']})
            context.update({'last_name':request.POST['last_name']})
            context.update({'username':request.POST['username']})
            return render(request, "cosmo_user/register.html", context=context)
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.success(request, "Please choose different username.", extra_tags="0")
            context = {}
            context.update({'first_name':request.POST['first_name']})
            context.update({'last_name':request.POST['last_name']})
            context.update({'email':request.POST['email']})
            return render(request, "cosmo_user/register.html", context=context)
        else:
            try:
                if register_user.register_django_user(request):
                    user = User.objects.get(username=request.POST['username'])
                    
                    if register_user.register_cosmo_user(user=user):
                        messages.success(request, "You have been successfully register.", extra_tags="1")
                        return HttpResponseRedirect(reverse('user-index'))
                    else:
                        try:
                            user.delete()
                            messages.success(request, "Could not register. Please try again.", extra_tags="1")
                            return HttpResponseRedirect(reverse('user-register'))
                        except Exception as e:
                            print(e)
                            return render(request, 'cosmo_user/register.html')
                else:
                    messages.success(request, "Could not register. Please try again.", extra_tags="1")
                    return HttpResponseRedirect(reverse('user-register'))

            except Exception as e:
                print(e)
                messages.success(request, "Could not register. Please try again.", extra_tags="1")
                return HttpResponseRedirect(reverse('user-register'))
            


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    return HttpResponseRedirect(reverse('verified-user-view'))


def verification(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
    cosmo_code_expiry = cosmo_user.expiry
    current_date_time = datetime.now()
    
    diff = abs(current_date_time.date() - cosmo_code_expiry.date()).days

    if (cosmo_user.token == int(request.POST.get('code'))):
        if diff > 1:
            messages.success(request,"Code has been expired. ", extra_tags="0")
            return HttpResponseRedirect(reverse('not-verified-index'))
        else:
            cosmo_user.verified = True
            cosmo_user.save()
            messages.success(request, "You have been successfully verified. Thank You.", extra_tags="1")
            return HttpResponseRedirect(reverse('verified-user-view'))
    else:
        messages.success(request,"Code does not matched. Please try again.", extra_tags="2")
        return HttpResponseRedirect(reverse('not-verified-index'))
