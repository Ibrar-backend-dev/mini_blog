from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Country(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        self.name = self.name.capitalize().strip()

        if not self.name:
            raise ValidationError("Country name cannot be empty.") 
        
        if Country.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError("Country with this name already exists.")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        