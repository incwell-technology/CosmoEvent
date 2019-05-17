from cosmo_user import models as cosmo_model

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