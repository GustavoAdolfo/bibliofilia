from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='livros'),
    path('<int:lvid>', views.livro, name='livro')
]
