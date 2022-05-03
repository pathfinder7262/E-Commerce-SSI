from pickle import TRUE
from pydoc import describe
from statistics import mode
from django.db import models
from matplotlib import image
from pandas import describe_option

# Create your models here.
class category(models.Model):  #table name category
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length = 255,blank=TRUE)
    image= models.ImageField(upload_to = 'image/categary',blank = True)


    def __str__(self):
        return self.name