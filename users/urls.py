"""Define os padrões de url para usuarios."""
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, path
from . import views
from django.conf.urls import url, include
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeForm

app_name = 'usuario'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(),
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    # url(r'^changepassword/$', views.changepassword, name='changepassword'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('usuario:password_reset_done'),
            template_name='users/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('usuario:password_reset_complete'),
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path('reset', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('usuario:reset'),
        template_name='users/changepassword.html'
    ), name='changepassword'),
]
