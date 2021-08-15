from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='autores'),
    path('<int:aid>', views.autor, name='autor'),
    path('busca/', views.busca, name="busca")
]
