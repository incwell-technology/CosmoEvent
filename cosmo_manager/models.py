from django.db import models

# Create your models here.

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


class TopView(SingletonModel):
    youtube_link = models.CharField(max_length=300, null=False, blank=False, default="nothing")
    fullName = models.CharField(max_length=300, null=False, blank=False, default="nothing")
    views = models.CharField(max_length=300, null=False, blank=False, default="0")

    def __str__(self):
        return f'{self.fullName}'

