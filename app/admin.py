from django.contrib import admin
from .models import Movie,Review

# Register your models here on every models that is made on models.py
admin.site.register(Movie)
admin.site.register(Review)