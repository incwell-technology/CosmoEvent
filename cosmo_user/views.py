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
            return render(request, 'cosmo_user/login.html', {'message': 'Login To Participate', 'title': 'Cosmo Event | Login'})
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
        error = []
        context = {}
        context.update({'first_name':request.POST['first_name']})
        context.update({'last_name':request.POST['last_name']})
        context.update({'phone':request.POST['phone']})
        if request.POST['email'] == "":
            error.append('Email field is required.')

        if request.POST['first_name'] == "":
            error.append('First Name is required.')

        if request.POST['last_name'] == "":
            error.append('Last Name is required.')

        if request.POST['username'] == "":
            error.append('Username field is required.')

        if request.POST['password'] == "":
            error.append('Password field is required.')

        if request.POST['phone'] == "":
            error.append('Phone number field is required.')

        if cosmo_models.CosmoUser.objects.filter(primaryPhone=request.POST['phone']):
            error.append('User with this phone number already exists.')

        if User.objects.filter(email=request.POST['email']).exists():
            error.append('User with this email id already exists.')
            context.update({'username':request.POST['username']})
        
        if User.objects.filter(username=request.POST['username']).exists():
            error.append('Choose another username.')
            context.update({'email':request.POST['email']})
        
        if len(request.POST['password'])<8:
            error.append('Password must be atleast 8 character long.')
        
        if len(request.POST['phone'])<7:
            error.append('Phone number must be atleast 7 character long.')

        if error:
            context.update({'error':error})
            return render(request, "cosmo_user/register.html", context=context)
        else:
            try:
                if register_user.register_django_user(request):
                    messages.success(request, "You have been successfully register. Please check your email to verify.", extra_tags="1")
                    return HttpResponseRedirect(reverse('not-verified-index'))
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

    try:
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        if cosmo_user.verified:
            return HttpResponseRedirect(reverse('verified-user-view'))
        else:
            return HttpResponseRedirect(reverse('not-verified-index'))
    except cosmo_models.CosmoUser.DoesNotExist:
        return HttpResponseRedirect(reverse('user-login'))


def verification(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    try:
        
        if not request.POST['code']:
            messages.success(request, "Invalid Verification Code.", extra_tags="0")
            return HttpResponseRedirect(reverse('not-verified-index'))

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
    except Exception as e:
        print(e)
        messages.success(request,"Code does not matched. Please try again.", extra_tags="2")
        return HttpResponseRedirect(reverse('not-verified-index'))



    