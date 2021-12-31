"""Visualizações dos empréstimos."""
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from emprestimos.models import Emprestimo, Espera, AgendamentoDevolucao
from django.core.paginator import Paginator
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib import messages, auth
import operator
from django.http import Http404
from biblioteca.models import Livro
from datetime import datetime, date, timedelta
import pytz
from django.contrib.messages.constants import ERROR, SUCCESS
from django.contrib.auth.decorators import login_required
from emprestimos.forms import AgendamentoForm, EmprestimoForm, ReservaForm


weekDays = ("Segunda-Feira", "Terça-Feira", "Quarta-Feira",
            "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo")


@login_required(login_url='/user/login/')
def solicitar(request, livro_id):
    """Inicia uma nova solicitacao de empréstimo."""
    if request.method != 'POST':
        livro = Livro.objects.get(id=livro_id)
        if not livro or not livro.disponivel:
            livro = None
            messages.add_message(
                request, ERROR, 'Livro não encontrado', extra_tags='safe')
            return HttpResponseRedirect(reverse('emprestimos:index'))

        naive = datetime.utcnow()
        aware = pytz.timezone('America/Sao_Paulo').localize(naive)
        dia_semana = aware.date().weekday()
        intervalo = 5 - dia_semana
        data_retirada = aware.date() + timedelta(intervalo)
        emprestimo = Emprestimo()
        emprestimo.data_previsao_retirada_1 = data_retirada
        emprestimo.data_previsao_retirada_2 = data_retirada + timedelta(1)
        emprestimo.data_prevista_devolucao_1 = data_retirada + \
            timedelta(14)
        emprestimo.data_prevista_devolucao_2 = data_retirada + \
            timedelta(15)
        emprestimo.data_solicitacao = aware
        usuario = auth.get_user(request)
        emprestimo.user = usuario
        emprestimo.nome_usuario_historico = usuario.get_username()
        emprestimo.livro = livro
        emprestimo.titulo_livro_historico = str(livro)
        emprestimo.observacoes = ''
        dados = {}
        for item in vars(emprestimo):
            dados.update({item: getattr(emprestimo, item)})
        context = {}
        context['form'] = EmprestimoForm(dados)
        return render(request, 'emprestimos/novo.html', context)
        # return render(request, 'emprestimos/novo.html', dados)

    form = EmprestimoForm(data=request.POST)
    if form.is_valid():
        novo_emprestimo = Emprestimo()
        novo_emprestimo.data_previsao_retirada_1 = form.cleaned_data['data_previsao_retirada_1']
        novo_emprestimo.data_previsao_retirada_2 = form.cleaned_data['data_previsao_retirada_2']
        novo_emprestimo.data_solicitacao = form.cleaned_data['data_solicitacao']
        novo_emprestimo.titulo_livro_historico = form.cleaned_data['titulo_livro_historico']
        novo_emprestimo.nome_usuario_historico = form.cleaned_data['nome_usuario_historico']
        novo_emprestimo.user = auth.get_user(request)
        novo_emprestimo.livro = Livro.objects.get(
            id=form.cleaned_data['livro_id'])
        novo_emprestimo.observacoes = form.cleaned_data['observacoes']
        novo_emprestimo.data_prevista_devolucao_1 = form.cleaned_data[
            'data_prevista_devolucao_1']
        novo_emprestimo.data_prevista_devolucao_2 = form.cleaned_data[
            'data_prevista_devolucao_2']
        novo_emprestimo.save()
        messages.add_message(request,
                             SUCCESS,
                             str(novo_emprestimo),
                             extra_tags='safe')
        return HttpResponseRedirect(reverse('emprestimos:index'))

    messages.add_message(request,
                         ERROR,
                         'Não foi possível solicitar o empréstimo.',
                         extra_tags='safe')
    context = {'form': form}
    return render(request, 'emprestimos/novo.html/25', context)


@login_required(login_url='/user/login/')
def index(request):
    user = auth.get_user(request)
    emprestimos = Emprestimo.objects.filter(
        user_id=user.id, cancelado=False).order_by('data_solicitacao')

    dados = {}
    if not emprestimos or not len(emprestimos):
        return render(request, 'emprestimos/index.html', dados)

    paginator = Paginator(emprestimos, 20)
    pg = request.GET.get('pg')
    dados = {'emprestimos': paginator.get_page(pg)}
    return render(request, 'emprestimos/index.html', dados)


def calcular_maior_data_prevista_para_reserva(maior_data):
    """Calcula a maior data prevista para reserva."""
    maior_data_prevista = maior_data
    maior_data_prevista = pytz.timezone(
        'America/Sao_Paulo').localize(maior_data_prevista)
    maior_data_prevista = maior_data_prevista + timedelta(15)
    if maior_data_prevista.weekday() == 6:
        maior_data_prevista = maior_data_prevista + timedelta(-1)
    elif maior_data_prevista.weekday() < 5:
        intervalo = maior_data_prevista.weekday() - 5
        maior_data_prevista = maior_data_prevista + timedelta(intervalo)
    return maior_data_prevista


@login_required(login_url='/user/login/')
def reservar(request, livro_id: int):
    """Reserva posição na fila de empréstimos."""
    try:
        if request.method != 'POST':
            livro = Livro.objects.get(id=livro_id)
            if not livro or not livro.disponivel:
                livro = None
                messages.add_message(
                    request, ERROR, 'Livro não encontrado', extra_tags='safe')
                return HttpResponseRedirect(reverse('emprestimos:index'))

            emprestimo = Emprestimo.objects.filter(
                livro_id=livro_id,
                data_efetiva_devolucao=None,
                data_cancelamento=None).order_by(
                    'data_prevista_devolucao_2').first()
            if not emprestimo:
                return HttpResponseRedirect(reverse('emprestimos:index', livro_id))

            fila_de_espera = Espera.objects.filter(
                livro_id=livro_id,
                emprestimo_efetuado=False,
                solicitacao_cancelada=False
            ).order_by('data_previsao_emprestimo_2').all()

            maior_data_prevista = calcular_maior_data_prevista_para_reserva(
                fila_de_espera.first().data_solicitacao.date())

            reserva = Espera()
            reserva.data_previsao_emprestimo_1 = maior_data_prevista
            reserva.data_previsao_emprestimo_2 = maior_data_prevista + \
                timedelta(1)
            reserva.data_solicitacao = pytz.timezone(
                'America/Sao_Paulo').localize(datetime.utcnow())
            reserva.livro = livro
            reserva.user = auth.get_user(request)
            reserva.emprestimo_efetuado = False
            reserva.solicitacao_cancelada = False
            reserva.observacoes = ''
            usuario = auth.get_user(request)
            emprestimo.nome_usuario_historico = usuario.get_username()
            emprestimo.livro = livro
            emprestimo.titulo_livro_historico = str(livro)

            # 4) Exibir página com o título do livro e as datas previtas e quantas
            # pessoas estão na fila e a provável data disponível para o solicitante.
            # 5) Salvar a solicitação com as datas apresentadas de reserva e
            # empréstimos e alguma observação se houver.

            dados = {'tamanho_fila': len(fila_de_espera), 'devolucoes_previstas': [
                emprestimo.data_prevista_devolucao_2.date(),
                [(item.data_previsao_emprestimo_2 +
                    timedelta(15)).date() for item in fila_de_espera]
            ]}
            for item in vars(emprestimo):
                dados.update({item: getattr(emprestimo, item)})
            context = {}
            context['form'] = ReservaForm(dados)
            return render(request, 'emprestimos/reserva.html', context)

        form = ReservaForm(data=request.POST)
        if form.is_valid():
            reserva = Espera()
            reserva.data_previsao_emprestimo_1 = form.cleaned_data['data_previsao_emprestimo_1']
            reserva.data_previsao_emprestimo_2 = form.cleaned_data['data_previsao_emprestimo_2']
            reserva.data_solicitacao = form.cleaned_data['data_solicitacao']
            reserva.titulo_livro_historico = form.cleaned_data['titulo_livro_historico']
            reserva.nome_usuario_historico = form.cleaned_data['nome_usuario_historico']
            reserva.user = auth.get_user(request)
            reserva.livro = Livro.objects.get(id=form.cleaned_data['livro_id'])
            reserva.observacoes = form.cleaned_data['observacoes']
            reserva.emprestimo_efetuado = False
            reserva.solicitacao_cancelada = False
            reserva.save()
            messages.add_message(
                request,
                SUCCESS,
                'Livro reservado com sucesso!',
                extra_tags='safe')
            return HttpResponseRedirect(reverse('biblioteca:index'))
    except Exception as e:
        messages.add_message(request,
                             ERROR,
                             'Não foi possível realizar a reserva.',
                             extra_tags='safe')
        context = {'form': form}
        return render(request, 'emprestimos/reserva.html', context)


@login_required(login_url='/user/login/')
def espera(request):
    pass


@login_required(login_url='/user/login/')
def cancelar(request, id: int):
    try:
        emprestimo = Emprestimo.objects.get(id=id)
        if not emprestimo:
            messages.add_message(
                request,
                ERROR,
                'Solicitação de empréstimo não encontrada.',
                extra_tags='safe')
        else:
            emprestimo.cancelado = True
            naive = datetime.utcnow()
            aware = pytz.timezone('America/Sao_Paulo').localize(naive)
            emprestimo.data_cancelamento = aware
            emprestimo.save()
            messages.add_message(request,
                                 SUCCESS,
                                 'Solicitação cancelada com sucesso.',
                                 extra_tags='safe')
    except Exception:
        messages.add_message(request,
                             SUCCESS,
                             'Não foi possível realizar esta operação.',
                             extra_tags='safe')

    return HttpResponseRedirect(reverse('emprestimos:index'))


@login_required(login_url='/user/login/')
def agendar_devolucao(request, emprestimo_id):
    """Programa o agendamento da devolução."""
    if request.method != 'POST':
        try:
            user = auth.get_user(request)
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)
            agendamento = AgendamentoDevolucao()
            agendamento.user = user
            agendamento.emprestimo = emprestimo
            naive = datetime.utcnow()
            aware = pytz.timezone('America/Sao_Paulo').localize(naive)
            agendamento.data_agendamento = aware.date()
            agendamento.hora_inicial = 10
            agendamento.hora_final = 17
            dados = {}
            for item in vars(agendamento):
                dados.update({item: getattr(agendamento, item)})
            context = {}
            context['form'] = AgendamentoForm(dados)
            return render(request, 'emprestimos/agendamento.html', context)
        except Exception as ex:
            print(ex)
            messages.add_message(request,
                                 ERROR,
                                 'Não foi possível realizar esta operação.',
                                 extra_tags='safe')
            return HttpResponseRedirect(reverse('emprestimos:index'))
    else:
        form = AgendamentoForm(data=request.POST)
        if form.is_valid():
            agendamento = AgendamentoDevolucao()
            agendamento.data_agendamento = form.cleaned_data['data_agendamento']
            agendamento.hora_inicial = form.cleaned_data['hora_inicial']
            agendamento.hora_final = form.cleaned_data['hora_final']
            agendamento.user = auth.get_user(request)
            agendamento.emprestimo = Emprestimo.objects.get(
                id=form.cleaned_data['emprestimo_id'])
            agendamento.save()
            messages.add_message(request,
                                 SUCCESS,
                                 str(agendamento),
                                 extra_tags='safe')
            return HttpResponseRedirect(reverse('emprestimos:index'))

        messages.add_message(request,
                             ERROR,
                             'Não foi possível realizar o agendamento.',
                             extra_tags='safe')
        context = {'form': form}
        return render(request, 'emprestimos/agendamento.html', context)
