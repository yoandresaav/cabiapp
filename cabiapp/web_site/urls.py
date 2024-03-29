from django.urls import path, re_path
from django.contrib.admin.views.decorators import staff_member_required

from .views import (
    ReporteCreateView, ThanksView, SuperAdminView, 
    CreateAccountsView, activate, CabiAppPasswordResetView,
    VerMisReportesView, SuperVerUsers,
    username_check,
)

app_name = 'web_site'

urlpatterns = [
    path(
        '', 
        ReporteCreateView.as_view(),
        name='createreporte_page'
    ),

    path(
        'ver/mis/reportes/',
        VerMisReportesView.as_view(),
        name='ver_mis_reportes_page'
    ),

    ### Accounts functions

    path(
        'accounts/create/',
        CreateAccountsView.as_view(),
        name='create_accounts_page'
    ),

    path(
        'accounts/password_reset/',
        CabiAppPasswordResetView.as_view(),
        name='password_reset'
    ),

    path(
        'thanks/',
        ThanksView.as_view(),
        name='thanks_page'
    ),

    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'
    ),

    path(
        'username/check/',
        username_check,
        name='username_check'
    ),

    ### Admin functions

    path(
        'check/view/reporte/',
        staff_member_required(SuperAdminView.as_view()),
        name='admin_page_reporte'
    ), # admin worker, no staff
    
    path(
        'check/view/users/',
        staff_member_required(SuperVerUsers.as_view()),
        name='admin_page_users'
    ), # admin worker, no staff
]