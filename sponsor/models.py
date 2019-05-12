from django.db import models

class Sponsor(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    photo = models.FileField(upload_to='cosmo_manager/static/cosmo_manager/site-data/sponsors', blank=False)
    link = models.CharField(max_length=500, null=True, blank=False)

    def __str__(self):
        return f'{self.name}'