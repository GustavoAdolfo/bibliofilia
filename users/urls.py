"""Define os padrões de url para usuarios."""
# from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy, path
from . import views
from django.conf.urls import url  # , include
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView

app_name = 'user'
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
    # url(
    #     r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     # 'django.contrib.auth.views.password_reset_confirm',
    #     PasswordResetConfirmView.as_view(),
    #     kwargs={'template_name': 'password_reset_confirm.html'},
    #     name='password_reset_confirm'),
    # path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #      views.password_reset_confirm,
    #      {'template_name': 'users/password_reset_confirm.html'},
    #      name='password_reset_confirm'),
    # path(
    #     r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     PasswordResetConfirmView.as_view(
    #         success_url=reverse_lazy('user:password_reset_confirm'),
    #         template_name='users/password_reset_confirm.html'),
    #     name='password_reset_confirm'
    # ),
    path(
        'password_reset_complete/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path('reset', PasswordChangeView.as_view(
        success_url=reverse_lazy('user:reset'),
        template_name='users/changepassword.html'
    ), name='changepassword'),
]
