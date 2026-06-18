from django.db import models

from apps.country.models import Country

# Create your models here.
class State(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete = models.CASCADE ,related_name='states')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name