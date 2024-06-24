from django.contrib import admin

# Register your models here.
from .models import Joke


@admin.register(Joke)
class AdminJoke(admin.ModelAdmin):
    list_display = ['user','created_at','updated_at']