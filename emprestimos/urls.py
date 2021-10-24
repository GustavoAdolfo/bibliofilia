"""Define os padrões de url para empréstimos."""
from django.conf.urls import url
from emprestimos import views


app_name = 'emprestimos'

urlpatterns = [
    # Página inicial (histórico do usuário)
    url(r'^$', views.index, name='index'),
    # Solicitar um empréstimo
    url(r'^novo/(?P<livro_id>\d+)$', views.solicitar, name='novo'),
    # Reservar (ser o próximo a pegar empréstimo)
    url(r'^reservar/(?P<livro_id>\d+)$', views.reservar, name='reservar'),
    # Filas em que o usuário está
    url(r'^espera/$', views.espera, name='espera'),
    # Cancelar solicitação de empréstimo
    url(r'^cancelar/(?P<id>\d+)$', views.cancelar, name='cancelar'),
    # Agendar a devolução
    url(r'^agendar/(?P<emprestimo_id>\d+)$',
        views.agendar_devolucao, name='agendar')
]
