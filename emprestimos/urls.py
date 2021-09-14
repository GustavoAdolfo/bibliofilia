"""Define os padrões de url para empréstimos."""
from django.conf.urls import url
from emprestimos import views


app_name = 'emprestimos'

urlpatterns = [
    # Página inicial (novo empréstimo)
    url(r'^novo/(?P<livo_id>\d+)$', views.novo, name='novo'),
    url(r'^/(?P<emprestimo_id>\d+)/$', views.index,
        name='emprestimo'),  # um empréstimo
    # Histórico de empréstimos do usuário
    url(r'^historico/$', views.historico, name='historico'),
    # Solicitar ser o próximo a pegar empréstimo
    url(r'^fila/entrar/$', views.entrar_na_fila, name='entrar_na_fila'),
    # Filas em que o usuário está
    url(r'^fila/$', views.filas_usuario, name='filas_usuario')
]
