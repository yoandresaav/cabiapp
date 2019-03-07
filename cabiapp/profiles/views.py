from django.shortcuts import render
from django.views.generic import UpdateView, DetailView

from .models import Profile


class ProfileShowView(DetailView):
    template_name = 'profiles/profile_show.html'
    model = Profile
    slug_field = 'slug'


class ProfileEditView(UpdateView):
    template_name = 'profiles/profile_edit.html'
    model = Profile
    slug_field = 'slug'
    fields = '__all__'

