# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile, CarProfile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email_confirmed', 'slug', 'phone')
    list_filter = ('email_confirmed',)
    search_fields = ('slug',)


@admin.register(CarProfile)
class CarProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'phone', 'user')
    list_filter = ('user',)