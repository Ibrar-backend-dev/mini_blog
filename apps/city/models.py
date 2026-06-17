from django.db import models

from mini_blog.apps import state
# Create your models here.

class City(models.Model):
    id = models.AutoField( primary_key=True)
    state_id = models.ForeignKey( state.State ,  on_delete = models.CASCADE , related_name= 'cities')
    name = models.CharField(  max_length=100 , unique= True)
    description = models.TextField( blank= True )