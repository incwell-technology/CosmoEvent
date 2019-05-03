from django.contrib import admin
from cosmo_user import models as cosmo_models


@admin.register(cosmo_models.CosmoUser)
class CosmoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'verified', 'votingCount')


@admin.register(cosmo_models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('cosmo_user', 'link', 'vote')
    ordering = ['-vote']


@admin.register(cosmo_models.CanParticipate)
class CanParticipateAdmin(admin.ModelAdmin):
    list_display = ['can_participate']