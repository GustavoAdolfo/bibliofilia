from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='livros'),
    path('<int:lvid>', views.livro, name='livro'),
    path('autor/<int:autor>', views.livros_autor, name='livro_autor'),
    path('busca/', views.busca, name="busca")
]
