from django.contrib import admin

# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'phone')
    list_filter = ('user',)
    search_fields = ('slug',)
