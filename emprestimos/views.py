"""Visualizações dos empréstimos."""
from django.shortcuts import render, redirect, get_object_or_404
from emprestimos.models import Emprestimo, Espera
from django.core.paginator import Paginator
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib import messages
import operator
from django.http import Http404
from biblioteca.models import Livro
from datetime import datetime, date, timedelta
import pytz
from django.contrib.auth.decorators import login_required


weekDays = ("Segunda-Feira", "Terça-Feira", "Quarta-Feira",
            "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo")


@login_required(login_url='usuario/login/')
def novo(request, id):
    """Inicia uma nova solicitacao de empréstimo."""
    if request.method != 'POST':
        livro = Livro.objects.get(id=id)
        if not livro or not livro.disponivel:
            livro = None

        dados = {}
        if livro:
            dados.update({'livro': livro})

        naive = datetime.utcnow()
        aware = pytz.timezone('America/Sao_Paulo').localize(naive)
        data_solicitacao = aware
        dados.update({'data_solicitacao': data_solicitacao})
        dia_semana = aware.date().weekday()
        intervalo = 5 - dia_semana
        data_retirada = aware.date() + timedelta(intervalo)
        dados.update({'data_retirada': data_retirada})
        # TODO: Montar tela com formulário para confirmar solicitação do
        # empréstimo e se não for encontrado o livro, avisar que o livro
        # não foi encontrado ou não informado
        return render(request, 'emprestimos/novo.html', dados)
    else:
        # TODO: Salvar o empréstimo do usuário e devolver página de confirmação
        # TODO: No index, listar os empréstimos em aberto, a lista de espera e o link para o histórico
        dados = {}
        return render(request, 'emprestimos/index.html', dados)


def index(request, id):
    pass


def historico(request):
    pass


def entrar_na_fila(request):
    pass


def filas_usuario(request):
    pass
