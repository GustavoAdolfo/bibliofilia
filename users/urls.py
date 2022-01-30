"""Define os padrões de url para usuarios."""
from django.urls import reverse_lazy, path
from . import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordChangeView
from .views import ActivateAccountView, ChangePasswordView

app_name = 'user'
urlpatterns = [
    url(r'^login/$', LoginView.as_view(),
        {'template_name': 'users/login.html'}, name='login'),
    path('activate/<uidb64>/<token>/',
         ActivateAccountView.as_view(), name='activate'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^perfil/$', views.perfil, name='perfil'),
    url(r'^editprofile/$', views.editprofile, name='editprofile'),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            success_url=reverse_lazy('user:password_reset_done'),
            template_name='users/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset_done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password_reset_complete/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('reset', ChangePasswordView.as_view(), name='changepassword'),
]
