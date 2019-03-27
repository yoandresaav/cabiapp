from django.urls import reverse_lazy
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
    fields = ('phone',)

    def get_success_url(self):
        slug = self.request.user.profile.slug
        url = reverse_lazy('profiles:profile_show_page', kwargs={'slug':slug})
        return str(url)  # success_url may be lazy

