
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

admin.site.site_title = 'Administración del Sitio CabiFleet'
admin.site.site_header = 'Administración del Sitio CabiFleet'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_site.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('profile/', include('profiles.urls')), 
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns