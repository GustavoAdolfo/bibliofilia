"""Define os padrões de url para usuarios."""
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views

app_name = 'usuario'

urlpatterns = [
    # Página de login
    url(r'^login/$', LoginView.as_view(),
        {'template_name': 'users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^cadastro/$', views.cadastro, name='cadastro'),
    url(r'^perfil/$', views.perfil, name='perfil')
]
