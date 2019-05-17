from cosmo_user import models as cosmo_model
from datetime import datetime


def is_verified(cosmo_user):
    if cosmo_user.verified:
        return True
    else:
        return False


def can_resend_code(cosmo_user):
    return True


def can_participate():
    instance = cosmo_model.CanParticipate.objects.get(id=1)
    print('asdasdsad',instance)
    return instance.can_participate


def get_all_users():
    users = cosmo_model.CosmoUser.objects.all()
    user_lists = []
    for cosmo_user in users:
        is_verified = "No"
        if cosmo_user.verified:
            is_verified = "Yes"

        participated = "No"
        try:
            if cosmo_model.Participant.objects.get(cosmo_user=cosmo_user):
                participated = "Yes"
        except cosmo_model.Participant.DoesNotExist:
            participated = "No"
        user_lists.append({
            'full_name':cosmo_user.user.get_full_name(),
            'email': cosmo_user.user.email,
            'phone1': cosmo_user.primaryPhone,
            'participated': participated,
            'votingCount':cosmo_user.votingCount,
            'verified': is_verified,
            'registered':datetime.strftime(cosmo_user.user.date_joined,'%Y-%m-%d %H:%M:%S'),
        })

    return user_lists


def get_all_participates():
    participates = cosmo_model.Participant.objects.all()
    participate_list = []

    for data in participates:
        is_selected = "No"
        if data.selected:
            is_selected = "Yes"
        participate_list.append({
            'fullName':data.cosmo_user.user.get_full_name(),
            'vote':data.vote,
            'contestantNumber':data.contestantNumber,
            'phone2':data.secondaryPhone,
            'Selected': is_selected,
            'Youtube Link':data.link,
            'Voting Video':data.voteVideo_link,
        })

    return participate_list


def is_admin(request):
    try:
        if request.user.is_superuser:
            return True
        else:
            return False
    except Exception as e:
        return False