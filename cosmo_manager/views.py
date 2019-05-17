from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from cosmo_user import models as cosmo_models
from django.contrib.auth import authenticate, login, logout
from cosmo_manager.common import cosmo_manager
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .forms import ParticipantForm
from cosmo_user.common.send_email_verification import send_verification_email
from cosmo_user.common.resend_verification_email import resend_verification_email
from datetime import datetime
from django.urls import reverse_lazy
from random import randint
import random
from django.db.models import Q
import csv
import calendar
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def verified_user_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    context = {}
    try:
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        if cosmo_user.verified:
            participate_status = cosmo_manager.can_participate()
            if participate_status == "1":
                participate_instance = cosmo_models.Participant.objects.none()
                participate_list = []
                try:
                    participate_instance = cosmo_models.Participant.objects.get(cosmo_user=cosmo_user)
                    participate_list.append({
                        'youtube_link':participate_instance.link,
                        # 'photo':participate_instance.photo.url.split('/static/')[1],
                        'vote':participate_instance.vote
                    })
                except cosmo_models.Participant.DoesNotExist:
                    pass
                if participate_instance:
                    context.update({'participate':participate_list})
                return render(request, "cosmo_manager/verified-view.html", context=context)
            elif participate_status == "2":
                return render(request, "cosmo_manager/participation-blocked.html")
        
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


def participate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    context = {}
    can_participates = cosmo_manager.can_participate()
    if can_participates == '1':
        try:
            cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
            if cosmo_manager.is_verified(cosmo_user):
                if can_participates == '1':
                    if request.method == "POST":
                        is_participated_user = cosmo_models.Participant.objects.filter(cosmo_user=cosmo_user).exists()
                        if is_participated_user:
                            messages.success(request, "You have already participated.", extra_tags="0")
                            if cosmo_manager.is_verified(cosmo_user):
                                return HttpResponseRedirect(reverse('verified-user-view'))
                            else:
                                return HttpResponseRedirect(reverse('not-verified-index'))
                        else:
                            # form = ParticipantForm(request.POST, request.FILES)
                            error = []
                            # if request.POST.get('photo') == "":
                            #     error.append('Photo field is required.')
                            if request.POST['youtube_link']  == "":
                                error.append('Youtube link is required.')
                            if request.POST['secondary_phone'] == "":
                                error.append('Secondary Phone is required.')
                            if error:
                                context.update({'error':error})
                                # form = ParticipantForm()
                                # context.update({'form':form})
                                return render(request, "cosmo_manager/participate.html", context=context)
                            else:
                                try:
                                    cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
                                    contestantNumber = 'CAC'+str(random.sample(range(1, 5), 1)[0])+str(random.sample(range(5, 10), 1)[0])+str(request.user.id)                                     
                                    
                                    if not cosmo_models.Tags.objects.filter(title=request.user.first_name):
                                        tags = cosmo_models.Tags.objects.create(title=request.user.first_name)

                                    if not cosmo_models.Tags.objects.filter(title=request.user.last_name):
                                        tags2 = cosmo_models.Tags.objects.create(title=request.user.last_name)
                                    if not cosmo_models.Tags.objects.filter(title=contestantNumber):
                                        tags3 = cosmo_models.Tags.objects.create(title=contestantNumber)
                                    if not cosmo_models.Tags.objects.filter(title=request.user.get_full_name()):
                                        cosmo_models.Tags.objects.create(title=request.user.get_full_name())

                                    participate_user = cosmo_models.Participant.objects.create(cosmo_user=cosmo_user,link=request.POST['youtube_link'],
                                    secondaryPhone=request.POST['secondary_phone'], contestantNumber=contestantNumber)
                                    for data in cosmo_models.Tags.objects.filter(Q(title=request.user.first_name) | Q(title=request.user.last_name) | Q(title=request.user.get_full_name()) | Q(title=contestantNumber)):
                                        participate_user.tags.add(data)

                                    if participate_user:
                                        messages.success(request, "Congratulations. You have successfully participated in Cosmo Event. Thank You.", extra_tags="1")
                                    else:
                                        messages.success(request, "Sorry. We are unable to save the records. Please try again.", extra_tags="0")
                                except Exception as e:
                                    print(e)
                                    messages.success(request, "Sorry. There was a problem on participating. Please try again.")

                                if cosmo_manager.is_verified(cosmo_user):
                                    return HttpResponseRedirect(reverse('verified-user-view'))
                                else:
                                    return HttpResponseRedirect(reverse('not-verified-index'))
                    else:
                        return render(request, "cosmo_manager/participate.html", context=context)
                else:
                    messages.success(request, "Sorry. Participation time is finished.", extra_tags="0")
                    if cosmo_manager.is_verified(cosmo_user):
                        return HttpResponseRedirect(reverse('verified-user-view'))
                    else:
                        return HttpResponseRedirect(reverse('not-verified-index'))
            else:
                return HttpResponseRedirect(reverse('not-verified-index'))
                
        except cosmo_models.CosmoUser.DoesNotExist:
            if request.user.is_authenticated:
                logout(request)
            return HttpResponseRedirect(reverse('user-login'))
    else:
        try:
            cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        except cosmo_models.CosmoUser.DoesNotExist:
            if request.user.is_authenticated:
                logout(request)
            return HttpResponseRedirect(reverse('user-login'))
            
        messages.success(request, "Sorry. Participation time is finished.", extra_tags="0")
        if cosmo_manager.is_verified(cosmo_user):
            return HttpResponseRedirect(reverse('verified-user-view'))
        else:
            return HttpResponseRedirect(reverse('not-verified-index'))

    
def resend_code(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    try:
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        if cosmo_manager.is_verified(cosmo_user):
            messages.success(request, "You have already been verified.", extra_tags="0")
            return HttpResponseRedirect(reverse('verified-user-view'))
        else:
            if cosmo_manager.can_resend_code(cosmo_user):
                suffix_verification_code = request.user.id+randint(1000, 9999)+request.user.id+2
                verification_code = random.sample(range(1000, 9999),1)[0]+suffix_verification_code

                date = datetime.now()
                update_details = {
                'recipient_email': request.user.email,
                'email_subject': 'Cosmo Acoustic Challenge | Resend: Registration verification code.',
                'email_body': f"""
                        Hi { request.user.get_full_name() }, <br/><br/>You have requested for new verification code. Your new verification code is:
                        <span style="text-align:center;text-weight:bold"><h1>{verification_code}</h1></span>
                        Please copy and paste the verification code to the link: <a href='http://{request.META['HTTP_HOST']}{reverse_lazy('not-verified-index')}'>Click Here</a> <br/><br/>

                        Date Requested: {date.strftime("%Y-%m-%d %H:%M:%S")}<br/>
                        <br/>
                        Thank You,<br/>
                        Cosmo Acoustic Challenge.<br/>
                        Arun Thapa Chowk, Jhamsikhel,<br/>
                        Nepal.<br/>
                        5555987, 6584658<br/>
                        """
                }
                if resend_verification_email(update_details, cosmo_user, verification_code):
                    messages.success(request, "New verification code has been send to your email. Please verify. Thank you.", extra_tags="1")
                else:
                    messages.success(request, "New verification code is unable to send. Please try again.", extra_tags="0")
                return HttpResponseRedirect(reverse('not-verified-index'))
            else:
                messages.success(request, "You have already request for new verification code. You cannot request again for new one. Thank You", extra_tags="0")
            return HttpResponseRedirect(reverse('not-verified-index'))
    except cosmo_models.CosmoUser.DoesNotExist:
        messages.success(request, "User does not exists.", extra_tags="0")
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('user-login'))


def search(request):
    cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)

    if not cosmo_manager.is_verified(cosmo_user):
        messages.success(request, "Please verify your account.", extra_tags="0")
        return HttpResponseRedirect(reverse('not-verified-index'))
    
    try:
        search_result = cosmo_models.Participant.objects.filter(tags__title__icontains=request.POST['search']).distinct()
        if search_result:
            context = {}
            context.update({'search_result':search_result})
            context.update({'recently_searched':request.POST['search']})
            context.update({'vote':cosmo_user.votingCount})
            return render(request, "cosmo_manager/search.html", context=context)
        else:
            messages.success(request, "Sorry. No result found. Please try again.", extra_tags="0")
            return HttpResponseRedirect(reverse('verified-user-view'))    
    except cosmo_models.Participant.DoesNotExist:
        messages.success(request, "Sorry. No result found. Please try again.", extra_tags="0")
        return HttpResponseRedirect(reverse('verified-user-view'))


def like_video(request, id):
    try:
        context = {}
        cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
        participate_instance = cosmo_models.Participant.objects.get(id=id)
        search_result = cosmo_models.Participant.objects.filter(tags__title__icontains=request.POST['need_to_search']).distinct()
        if not participate_instance:
            messages.success(request, "Contestant not found.", extra_tags="0")
        else:
            participate_instance.vote = participate_instance.vote+1
            participate_instance.save()
            cosmo_user.votingCount = cosmo_user.votingCount-1
            cosmo_user.save()
            messages.success(request, "Thank you for voting.", extra_tags="1")
        context.update({'search_result':search_result})
        context.update({'vote':cosmo_user.votingCount})
        return 
    except cosmo_models.Participant.DoesNotExist:
        pass


def admin(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))
    
    if cosmo_manager.is_admin(request):
        context = {}
        cosmo_users = cosmo_models.CosmoUser.objects.all().count()
        participates = cosmo_models.Participant.objects.all().count()
        context.update({'users':cosmo_users})
        context.update({'participates':participates})
        return render(request, "cosmo_manager/admin/index.html", context=context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))

def admin_users(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))

    if cosmo_manager.is_admin(request):
        return render(request, "cosmo_manager/admin/users.html")
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))

def admin_users_csv(request):
    today_month = datetime.today().month
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))

    if cosmo_manager.is_admin(request):
        all_users = cosmo_manager.get_all_users()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="All Users {calendar.month_name[today_month]}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Email', 'Primary Phone', 'Participated', 'Voting Left', 'Verified', 'Date Joined'])    
        counter = 1
        add_row = []
        for value in all_users:
            for j,k in value.items():
                if counter <= 7:
                    add_row.append(k)
                    counter+=1
            writer.writerow(add_row)
            counter=1    
            add_row = []
        return response
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))


def admin_participates(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))

    if cosmo_manager.is_admin(request):
        participates = cosmo_models.Participant.objects.order_by('-selected').all()
        context = {}
        context.update({'participates':participates})
        return render(request, "cosmo_manager/admin/participates.html", context=context)
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))        

def admin_participates_csv(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))
    today_month = datetime.today().month

    if cosmo_manager.is_admin(request):
        all_users = cosmo_manager.get_all_participates()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="All Participates {calendar.month_name[today_month]}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Full Name', 'Vote','Contestant Number', 'Secondary Phone', 'Selected', 'Youtube Link', 'Voting Video'])    
        counter = 1
        add_row = []
        for value in all_users:
            for j,k in value.items():
                if counter <= 6:
                    add_row.append(k)
                    counter+=1
            writer.writerow(add_row)
            counter=1    
            add_row = []
        return response
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))   


def admin_selected(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))

    if cosmo_manager.is_admin(request):

        try:
            user_data = cosmo_models.Participant.objects.get(id=id)
            if not user_data.selected:
                user_data.selected = True
                user_data.save()

            messages.success(request, str(user_data.contestantNumber)+"-"+str(user_data.cosmo_user.user.get_full_name())+" has been selected.", extra_tags="1")
            return HttpResponseRedirect(reverse('admin-participates'))
        except cosmo_models.Participant.DoesNotExist:
            messages.success(request, "Participate not found.", extra_tags="1")
            return HttpResponseRedirect(reverse('admin-participates'))
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))   


def admin_login(request):
    if request.method == "POST":
        try:
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user is None:
                messages.success(request, "Invalid Credentials", extra_tags="0")
                return HttpResponseRedirect(reverse('admin-login'))
            elif user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('admin'))
            else:
                messages.success(request, "Invalid Credentials", extra_tags="0")
                return HttpResponseRedirect(reverse('admin-login'))
        except Exception as e:
            messages.success(request, "Invalid Credentials", extra_tags="0")
            return HttpResponseRedirect(reverse('admin-login'))
    else:
        return render(request, "cosmo_manager/admin/login.html")


def admin_notSelected(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('admin-login'))

    if cosmo_manager.is_admin(request):
        try:
            user_data = cosmo_models.Participant.objects.get(id=id)
            if user_data.selected:
                user_data.selected = False
                user_data.save()

            messages.success(request, str(user_data.contestantNumber)+"-"+str(user_data.cosmo_user.user.get_full_name())+" has not been selected.", extra_tags="1")
            return HttpResponseRedirect(reverse('admin-participates'))
        except cosmo_models.Participant.DoesNotExist:
            messages.success(request, "Participate not found.", extra_tags="1")
            return HttpResponseRedirect(reverse('admin-participates'))
    else:
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('admin-login'))   