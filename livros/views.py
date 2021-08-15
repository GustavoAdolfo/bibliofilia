from django.shortcuts import render, redirect
from django.http import Http404
from .models import Livro
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
import operator


def index(request):
    ord = request.GET.get('ord')
    if ord and ord == '2':
        livros = Livro.objects.order_by('-titulo').filter(disponivel=True)
    elif ord and ord == '3':
        livros = Livro.objects.order_by('autor__nome').filter(disponivel=True)
    elif ord and ord == '4':
        livros = Livro.objects.order_by('-autor__nome').filter(disponivel=True)
    else:
        livros = Livro.objects.order_by('titulo').filter(disponivel=True)
    paginator = Paginator(livros, 20)
    pg = request.GET.get('pg')
    livros = paginator.get_page(pg)
    classificacoes = [
        {'id': '1', 'descricao': 'Título de A - Z'},
        {'id': '2', 'descricao': 'Título de Z - A'},
        {'id': '3', 'descricao': 'Autor de A - Z'},
        {'id': '4', 'descricao': 'Autor de Z - A'}
    ]
    return render(request, 'livros/index.html',
                  {'livros': livros, 'classificacao': classificacoes})


def livro(request, lvid):
    try:
        livro = Livro.objects.get(id=lvid)
        links = livro.link_amazon.split('|')
        if not livro.disponivel:
            raise Http404()
        return render(request, 'livros/livro.html',
                      {'livro': livro, 'links': links})
    except Livro.DoesNotExist:
        raise Http404()


def livros_autor(request, autor):
    try:
        livros = Livro.objects.filter(autor_id=autor)
        paginator = Paginator(livros, 10)
        pg = request.GET.get('pg')
        livros = paginator.get_page(pg)
        return render(request, 'livros/autor.html', {'livros': livros})
    except Livro.DoesNotExist:
        raise Http404()


def busca(request):
    try:
        termo = request.GET.get('termo')
        if not termo:
            messages.add_message(
                request, messages.ERROR, 'Informe um valor para a busca.')
            return redirect('livros')

        campos = Concat('titulo', Value(' '), 'subtitulo',
                        Value(' '), 'autor__nome')
        livros = Livro.objects.annotate(
            titulo_subtitulo=campos
        ).filter(
            titulo_subtitulo__icontains=termo,
            disponivel=True
        )
        if not livros or not len(livros):
            messages.add_message(
                request, messages.WARNING,
                'Nenhum livro encontrado com o termo solicitado.')
            return redirect('livros')

        ord = request.GET.get('ord')
        if ord and ord == '2':
            lista_ordenada = sorted(
                livros, key=operator.attrgetter('titulo'), reverse=True)
        elif ord and ord == '3':
            lista_ordenada = sorted(
                livros, key=operator.attrgetter('autor.nome'))
        elif ord and ord == '4':
            lista_ordenada = sorted(
                livros, key=operator.attrgetter('autor.nome'), reverse=True)
        else:
            lista_ordenada = sorted(livros, key=operator.attrgetter('titulo'))

        paginator = Paginator(lista_ordenada, 10)
        pg = request.GET.get('pg')
        livros = paginator.get_page(pg)
        classificacoes = [
            {'id': '1', 'descricao': 'Título de A - Z'},
            {'id': '2', 'descricao': 'Título de Z - A'},
            {'id': '3', 'descricao': 'Autor de A - Z'},
            {'id': '4', 'descricao': 'Autor de Z - A'}
        ]
        return render(request, 'livros/busca.html',
                      {'livros': livros, 'classificacao': classificacoes})
    except Livro.DoesNotExist:
        raise Http404()
