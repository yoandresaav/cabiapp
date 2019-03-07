from django.urls import include, path

from .views import ReporteCreateView, ThanksView, SuperAdminView, CreateAccountsView

app_name = 'web_site'

urlpatterns = [
    path('', ReporteCreateView.as_view(), name='createreporte_page'),
    path('accounts/create/', CreateAccountsView.as_view(), name='create_accounts_page'),    
    path('thanks/', ThanksView.as_view(), name='thanks_page'),
    path('entrar/', SuperAdminView.as_view(), name='admin_page'), # admin worker, no staff
]