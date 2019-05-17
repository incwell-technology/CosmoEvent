from django.contrib import admin
from cosmo_manager import models as cosmo_manager_models
# Register your models here.

@admin.register(cosmo_manager_models.TopView)
class TopViewAdmin(admin.ModelAdmin):
    list_display = ['youtube_link','views','fullName']