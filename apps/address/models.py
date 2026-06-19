from django.db import models

from apps.country.models import Country
from apps.state.models import State
from apps.city.models import City

# Create your models here.
class Address(models.Model):

    permanent_address = models.CharField(max_length=255 , blank=True)
    residential_address = models.CharField(max_length=255 , blank=True)

    country = models.ForeignKey (
        Country, on_delete=models.PROTECT, related_name='addresses'
        )
    state = models.ForeignKey (
        State, on_delete=models.PROTECT, related_name='addresses'
        )
    city = models.ForeignKey (
        City, on_delete=models.PROTECT, related_name='addresses'
        )
    postal_code = models.CharField(max_length=20, blank=True)

    