from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class CosmoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    photo = models.FileField(upload_to='cosmo_user/static/cosmo_user/site-data/profile-pictures', blank=True)
    votingCount = models.IntegerField(null=False, blank=False, default=25)
    verified = models.BooleanField(null=False, blank=False, default=False) #False = not verified
    token = models.IntegerField(null=False, blank=False)
    expiry = models.DateTimeField(default=datetime.now())
    primaryPhone = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Participant(models.Model):
    cosmo_user = models.OneToOneField(CosmoUser, on_delete=models.CASCADE, related_name="cosmo_participant")
    link = models.CharField(max_length=800, null=False, blank=False)
    voteVideo_link = models.CharField(max_length=800, null=True, blank=True)
    vote = models.IntegerField(null=False, blank=False, default=0)
    secondaryPhone = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.cosmo_user.user.get_full_name()}'
