"""Define os padrões de url para a biblioteca."""
from django.conf.urls import url
from biblioteca import views

app_name = 'biblioteca'

urlpatterns = [
    url(r'^$', views.index, name='index'), # Página inicial
    url(r'^livros/$', views.livros, name='livros'), # Lista de livros
    url(r'^livro/(?P<livro_id>\d+)/$', views.livro, name='livro'), # Página de um livro específico
    url(r'^livros/busca/$', views.livros_busca, name='livros_busca'), # Resultado da busca por livros
    url(r'^autores/$', views.autores, name='autores'), # Lista de autores
    url(r'^autor/(?P<autor_id>\d+)/$', views.autor, name='autor'), # Página de um autor específico
    url(r'^autores/busca/$', views.autores_busca, name='autores_busca'), # Resultado da busca por autores
    url(r'^sobre/$', views.sobre, name='sobre'), # Página de informacoes
]