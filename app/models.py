from ast import keyword
from operator import imod
from statistics import mode
from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#every time we make changes in model we need to do makemigrations and migrate
class Movie(models.Model):
    title = models.CharField(max_length=100)
    budget = models.BigIntegerField(blank=True,null = True)
    genres = models.TextField(blank=True,null=True)
    favourite= models.ManyToManyField(User, related_name='favourite')

    keywords = models.TextField(blank=True, null=True)
    overview = models.TextField(blank=True,null=True)
    tagline = models.TextField(blank=True,null=True)
    cast = models.TextField(blank=True,null=True)
    director = models.CharField(max_length=100, blank=True,null=True)

    def __str__(self):
        return self.title
    
    def get_budget_in_yen(self):
        return self.budget * 123

class Review(models.Model):
    review = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    #movie ra user data extraction
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='movie')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')

