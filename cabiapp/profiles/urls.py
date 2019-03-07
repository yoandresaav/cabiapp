from django.urls import include, path

from .views import ProfileEditView, ProfileShowView

app_name = 'profiles'

urlpatterns = [
    path('<slug:slug>/', ProfileShowView.as_view(), name='profile_show_page'),
    path('edit/<slug:slug>/', ProfileEditView.as_view(), name='profile_edit_page'),
    
]