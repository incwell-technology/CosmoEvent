from django import forms
from cosmo_user import models as cosmo_models

class ParticipantForm(forms.ModelForm):

    class Meta:
        model = cosmo_models.Participant
        fields = ['photo']
