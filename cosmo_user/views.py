from datetime import datetime
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cosmo_user import models as cosmo_models
from django.contrib import messages


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
    context = {
        'departments': Department.objects.all()
    }
    leaves = get_all_leaves_unseen()
    context.update({'leave_notify':leaves})
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))
    if not is_leave_issuer(request.user):
        return HttpResponseRedirect(reverse('leave_manager_dashboard'))
    routes = get_formatted_routes(get_routes(request.user), active_page='register user')
    context.update({'routes': routes})
    if request.method == 'GET':
        if not request.user.is_authenticated:
            url = reverse('user-login')
            return HttpResponseRedirect(url)
        return render(request, 'lms_user/register.html', context=context)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            url = reverse('user-login')
            return HttpResponseRedirect(url)
        else:
            try:
                if register_django_user(request):
                    user = User.objects.get(username=request.POST['username'])
                    department = Department.objects.get(id=int(request.POST['department']))
                    lms_user_details = {
                        'user': user,
                        'phone_number': request.POST['phone_number'],
                        'department': department,
                        'leave_issuer': department.head_of_department,
                        'date_of_birth': datetime.strptime(request.POST['date_of_birth'], '%Y-%m-%d'),
                        'joined_date': datetime.strptime(request.POST['joined_date'], '%Y-%m-%d')
                    }
                    if register_lms_user(user_details=lms_user_details):
                        return HttpResponseRedirect(reverse('user-index'))
                    else:
                        try:
                            user.delete()
                            context.update({'message': 'Could register to LMS. Please contact Admin or try again later'})
                            return render(request, 'lms_user/register.html', context=context)
                        except Exception as e:
                            print(e)
                            return render(request, 'lms_user/register.html', context=context)
                else:
                    context.update({'message': 'Could register to Django. Please contact Admin or try again later'})
                    return render(request, 'lms_user/register.html', context=context)

            except Exception as e:
                print(e)
                context.update({'message': 'Could not register. Please contact Admin or try again later'})
                return render(request, 'lms_user/register.html', context=context)


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
