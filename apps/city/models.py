from django.db import models

from apps.state.models import State
# Create your models here.

class City(models.Model):
    id = models.AutoField( primary_key=True)
    state = models.ForeignKey( State ,  on_delete = models.CASCADE , related_name= 'cities')
    name = models.CharField(  max_length=100 , unique= True)
    description = models.TextField( blank= True )