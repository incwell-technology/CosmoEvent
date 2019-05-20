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
    resend_code = models.BooleanField(null=False, blank=False, default=True) #False = cannot resend #True = can resend

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Tags(models.Model):
    title = models.CharField(max_length=800, null=False, blank=False, default="Cosmo")

    def __str__(self):
        return f'{self.title}'

        
selected_choice = (
    (True, 'Is Selected'),
    (False, 'Not Selected')
)

class Participant(models.Model):
    cosmo_user = models.OneToOneField(CosmoUser, on_delete=models.CASCADE, related_name="cosmo_participant")
    photo = models.ImageField(upload_to='cosmo_user/static/cosmo_user/site-data/profile-pictures', null=True, blank=True)
    link = models.CharField(max_length=800, null=False, blank=False)
    voteVideo_link = models.CharField(max_length=800, null=True, blank=True)
    vote = models.IntegerField(null=False, blank=False, default=0)
    secondaryPhone = models.IntegerField(null=False, blank=False, default="984000000")
    contestantNumber = models.CharField(max_length=800, null=False, blank=False)
    tags = models.ManyToManyField(Tags,related_name="participant_tags")
    selected = models.BooleanField(choices=selected_choice, null=False, blank=False, default=False)

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
    ('1', 'Allow Participant'),
    ('2', 'Block Participant'),
    ('3', 'Cast Vote'),
    ('4', 'Stop Vote'),
)

class CanParticipate(SingletonModel):
    can_participate = models.CharField(max_length=10, choices=participate_choice, null=False, blank=False)

    def __str__(self):
        return f'{self.can_participate}'