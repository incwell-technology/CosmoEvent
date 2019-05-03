from cosmo_user import models as cosmo_model

def is_verified(cosmo_user):
    if cosmo_user.verified:
        return True
    else:
        return False



    