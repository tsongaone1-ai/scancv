from django.db import models

class Ecv(models.Model):
    name = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    skill = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name