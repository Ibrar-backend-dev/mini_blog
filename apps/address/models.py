from django.conf import settings
from django.db import models

from apps.country.models import Country
from apps.state.models import State
from apps.city.models import City


class Address(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="address",
        null=True,
        blank=True,
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name="addresses",
    )
    state = models.ForeignKey(
        State,
        on_delete=models.PROTECT,
        related_name="addresses",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name="addresses",
    )

    permanent_address = models.CharField(max_length=255, blank=True)
    residential_address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return f"{self.permanent_address}, {self.residential_address}, {self.city.name}, {self.state.name}, {self.country.name}, {self.postal_code}"

