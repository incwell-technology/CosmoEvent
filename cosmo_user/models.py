from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class CosmoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    votingCount = models.IntegerField(null=False, blank=False, default=25)
    verified = models.BooleanField(null=False, blank=False, default=False) #False = not verified
    token = models.IntegerField(null=False, blank=False)
    expiry = models.DateTimeField(default=datetime.now())
    primaryPhone = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Participant(models.Model):
    cosmo_user = models.OneToOneField(CosmoUser, on_delete=models.CASCADE, related_name="cosmo_participant")
    photo = models.ImageField(upload_to='cosmo_user/static/cosmo_user/site-data/profile-pictures', null=False, blank=False)
    link = models.CharField(max_length=800, null=False, blank=False)
    voteVideo_link = models.CharField(max_length=800, null=True, blank=True)
    vote = models.IntegerField(null=False, blank=False, default=0)
    secondaryPhone = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.cosmo_user.user.get_full_name()}'


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

participate_choice = (
    (True, 'Allow Participant'),
    (False, 'Block Participant'),
)

class CanParticipate(SingletonModel):
    can_participate = models.BooleanField(max_length=1, choices=participate_choice, null=False, blank=False, default=True)

    def __str__(self):
        return f'{self.can_participate}'