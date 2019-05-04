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


def participate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user-login'))

    context = {}
    can_participates = cosmo_models.CanParticipate.objects.get(id=1)
    if can_participates.can_participate:
        try:
            cosmo_user = cosmo_models.CosmoUser.objects.get(user=request.user)
            if cosmo_manager.is_verified(cosmo_user):
                can_participates = cosmo_models.CanParticipate.objects.all()
                if can_participates:
                    if request.method == "POST":
                        is_participated_user = cosmo_models.Participant.objects.filter(cosmo_user=cosmo_user).exists()
                        if is_participated_user:
                            messages.success(request, "You have already participated.", extra_tags="0")
                            if cosmo_manager.is_verified(cosmo_user):
                                return HttpResponseRedirect(reverse('verified-user-view'))
                            else:
                                return HttpResponseRedirect(reverse('not-verified-index'))
                        else:
                            form = ParticipantForm(request.POST, request.FILES)
                            error = []
                            if request.POST.get('photo') == "":
                                error.append('Photo field is required.')
                            if request.POST['youtube_link']  == "":
                                error.append('Youtube link is required.')
                            
                            if error:
                                context.update({'error':error})
                                form = ParticipantForm()
                                context.update({'form':form})
                                return render(request, "cosmo_manager/participate.html", context=context)
                            else:
                                try:
                                    if form.is_valid():
                                        participant_user = form.save(commit=False)
                                        participant_user.cosmo_user = cosmo_user
                                        participant_user.link = request.POST['youtube_link']
                                        if request.POST['secondary_phone']:
                                            participant_user.secondaryPhone = request.POST['secondary_phone']
                                        participant_user.save()
                                        messages.success(request, "Congratulations. You have successfully participated in Cosmo Event. Thank You.", extra_tags="1")
                                    else:
                                        context.update({'form':form})
                                        return render(request, "cosmo_manager/participate.html", context=context)
                                except Exception as e:
                                    print(e)
                                    messages.success(request, "Sorry. There was a problem on participating. Please try again.")

                                if cosmo_manager.is_verified(cosmo_user):
                                    return HttpResponseRedirect(reverse('verified-user-view'))
                                else:
                                    return HttpResponseRedirect(reverse('not-verified-index'))
                    else:
                        form = ParticipantForm()
                        context.update({'form':form})
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
                verification_code = 2580    

                update_details = {
                'recipient_email': request.user.email,
                'email_subject': 'Cosmo Event | Resend: Registration verification code.',
                'email_body': f"""
                        Hi { request.user.get_full_name() }, You have requested to send new verification code. Your new verification code is:
                    <input type='text' value='{verification_code}' disabled/>
                        Please copy and paste the verification code to the link: http://localhost:8000/home/verify

                        Date: {datetime.now()}
                        Note: You have request for new verification code. You will not be able to login if this code expires.

                        Thank You,
                        Cosmo Event.
                        Arun Thapa Chowk, Jhamsikhel,
                        Nepal.
                        5555987, 6584658
                        """
                }
                if resend_verification_email(update_details, cosmo_user, verification_code):
                    messages.success(request, "New verification code has been send to your email. Please verify. Thank you.", extra_tags="1")
                else:
                    messages.success(request, "New verification code is unable to send. Please try again.", extra_tags="0")
                return HttpResponseRedirect(reverse('not-verified-index'))
            else:
                messages.success(request, "You have already request for new verification code. You cannot request again for new one. Thank You", extra_tags="0")
    except cosmo_models.CosmoUser.DoesNotExist:
        messages.success(request, "User does not exists.", extra_tags="0")
        if request.user.is_authenticated:
            logout(request)
        return HttpResponseRedirect(reverse('user-login'))
