"""Define os padrões de url para usuarios."""
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
import django.contrib.auth.urls

app_name = 'usuario'

urlpatterns = [
    # Página de login
    url(r'^login/$', LoginView.as_view(),
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),

    url(r'^password_reset/$',
        PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'),
    url(r'^password-reset-confirm/(?P<uidb64>\.+)/(?P<token>\.+)/$',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),

    # url(r'^', include('django.contrib.auth.urls')),
    # url(r'^reset/(?P<uidb64>)/(?P<token>)/$',
    #     PasswordResetConfirmView.as_view()),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     PasswordResetConfirmView.as_view()),

    url(r'^password_reset_done/$', PasswordResetDoneView.as_view()),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view()),
]
