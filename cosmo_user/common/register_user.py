from cosmo_user import models as cosmo_models
from datetime import datetime
from django.contrib.auth.models import User
from cosmo_user.common.send_email_verification import send_verification_email
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from random import randint

def register_django_user(request):
    try:
        user = User.objects.create(username=request.POST['username'],
                                   email=request.POST['email'], first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'])
        user.set_password(request.POST['password'])
        user.save()
        verification_code = randint(10000, 99999)+user.id
        date = datetime.now()
        update_details = {
        'recipient_email': request.POST['email'],
        'email_subject': 'Cosmo Event | Registration verification code.',
        'email_body': f"""
                Hi {request.POST['first_name']} {request.POST['last_name']},<br/><br/> You have registered in Cosmo Event. Your verification code is:
                 <span style="text-align:center;text-weight:bold"><h1>{verification_code}</h1></span><br/><br/>
                Please copy and paste the verification code to the link:<a href='http://{request.META['HTTP_HOST']}{reverse_lazy('not-verified-index')}'>Click Here</a><br/><br/>

                Date Registered: {date.strftime("%Y-%m-%d %H:%M:%S")}<br/>
                Note: This verification code expires soon. Please verify soon.</br>
                Thank You,<br/>
                Cosmo Event.<br/>
                Arun Thapa Chowk, Jhamsikhel,<br/>
                Nepal.<br/>
                5555987, 6584658
                """
        }
        if send_verification_email(update_details, user):
            user = User.objects.get(username=request.POST['username'])
        
            if register_cosmo_user(user=user, phone=request.POST['phone'], verification_code=verification_code):
                users = authenticate(request, username=request.POST['username'], password=request.POST['password'])
                if users:
                    login(request, users)
                    return True
                else:
                    return False
            else:
                try:
                    user.delete()
                    return False
                except Exception as e:
                    print(e)
                    return render(request, 'cosmo_user/register.html')
            return True
        else:
            user.delete()
            return False
       

    except Exception as e:
        if user:
            user.delete()
        print(e)
        return False

def register_cosmo_user(user, phone, verification_code):
        try:
            if cosmo_models.CosmoUser.objects.create(user=user, primaryPhone=phone, votingCount=25,verified=False,resend_code = True, expiry=datetime.now(), token=verification_code):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

