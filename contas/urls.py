from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='contas'),
    path('perfil/<int:id>', views.perfil, name='perfil'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('painel/', views.painel, name='painel'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('registrar/', views.registrar, name='registrar'),
    path('atualizar_perfil/', views.registrar, name='atualizar_perfil')
]
