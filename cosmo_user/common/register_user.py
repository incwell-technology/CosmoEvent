from cosmo_user import models as cosmo_models
from datetime import datetime
from django.contrib.auth.models import User


def register_django_user(request):
    try:
        user = User.objects.create(username=request.POST['username'],
                                   email=request.POST['email'], first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'])
        user.set_password(request.POST['password'])
        user.save()
        return True

    except Exception as e:
        print(e)
        return False

def register_cosmo_user(user, phone):
        try:
            cosmo_models.CosmoUser.objects.create(user=user, primaryPhone=phone, votingCount=25,verified=False,token=2580,expiry=datetime.now())
            return True
        except Exception as e:
            print(e)
            return False