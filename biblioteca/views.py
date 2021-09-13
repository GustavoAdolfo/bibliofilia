"""Visualizações da biblioteca."""
from django.shortcuts import render, redirect, get_object_or_404
from biblioteca.models import Autor, Livro
from django.core.paginator import Paginator
from django.db.models import Value  # , Q
from django.db.models.functions import Concat
from django.contrib import messages
import operator
from django.http import Http404
import json
from django.contrib.staticfiles.storage import staticfiles_storage


url = staticfiles_storage.path('countries.json')
countries = []
try:
    with open(url, "r") as cdata:
        content = ''.join(cdata.readlines())
        countries = json.loads(content)
        countries = list(filter(lambda x: 'pt-br' in x, countries))
except Exception:
    pass


# pylint: disable=maybe-no-member
def index(request):
    """Define a página inicial da Minhoteca."""
    num_autores = Autor.objects.all().filter(
        livro__disponivel=True).distinct('nome').count()
    num_livros = Livro.objects.filter(disponivel=True).count()
    return render(request, 'biblioteca/index.html',
                  {'num_livros': num_livros, 'num_autores': num_autores})


def sobre(request):
    """Página de ajuda e informações gerais."""
    return render(request, 'home/sobre.html')


def livros(request):
    """Retorna os livros cadastrados."""
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
    return render(request, 'biblioteca/livros.html',
                  {'livros': livros, 'classificacao': classificacoes})


def livro(request, livro_id):
    """Retorna os dados livro solicitado."""
    try:
        livro = Livro.objects.get(id=livro_id)
        links = livro.link_amazon.split('|')
        if not livro.disponivel:
            raise Http404()
        return render(request, 'biblioteca/livro.html',
                      {'livro': livro, 'links': links})
    except Livro.DoesNotExist:
        raise Http404()


def livros_autor(request, autor_id):
    """Retorna os livros de um autor específico"""
    try:
        livros = Livro.objects.filter(autor_id=autor_id)
        paginator = Paginator(livros, 10)
        pg = request.GET.get('pg')
        livros = paginator.get_page(pg)
        return render(request,
                      'biblioteca/livros_autor.html', {'livros': livros})
    except Livro.DoesNotExist:
        raise Http404()


def livros_busca(request):
    """Retorna o resultado de uma busca por livros."""
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
        return render(request, 'biblioteca/livros_busca.html',
                      {'livros': livros, 'classificacao': classificacoes})
    except Livro.DoesNotExist:
        raise Http404()


def autores(request):
    """Lista autores cadastrados."""
    ord = request.GET.get('ord')
    autores = Autor.objects.order_by(
        'nome').filter(livro__disponivel=True).distinct('nome')
    if ord and ord == '2':
        lista_ordenada = sorted(
            autores, key=operator.attrgetter('nome'), reverse=True)
    elif ord and ord == '3':
        lista_ordenada = sorted(
            autores, key=operator.methodcaller('count_livros'), reverse=True)
    elif ord and ord == '4':
        lista_ordenada = sorted(
            autores, key=operator.methodcaller('count_livros'))
    else:
        lista_ordenada = sorted(autores, key=operator.attrgetter('nome'))

    lista_autores = []
    for autor in lista_ordenada:  # autores:
        dic_autor = {'autor': autor}
        pais = next(filter(
            lambda x: x['pt-br'] == autor.pais_origem, countries), None)
        if pais:
            dic_autor.update(
                {'flag': 'data:image/png;base64, {0}'.format(pais['flag'])})
        else:
            dic_autor.update({'flag': ''})
        lista_autores.append(dic_autor)
    paginator = Paginator(lista_autores, 20)
    pg = request.GET.get('pg')
    autores = paginator.get_page(pg)
    classificacoes = [
        {'id': '1', 'descricao': 'Nome de A - Z'},
        {'id': '2', 'descricao': 'Nome de Z - A'},
        {'id': '3', 'descricao': 'Mais livros'},
        {'id': '4', 'descricao': 'Menos livros'}
    ]
    return render(request, 'biblioteca/autores.html',
                  {'autores': autores, 'classificacao': classificacoes})


def autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    livros = autor.livro_set.filter(autor_id=autor_id,
                                    disponivel=True)
    dic_autor = {'autor': autor}
    pais = next(filter(
        lambda x: x['pt-br'] == autor.pais_origem, countries), None)
    if pais:
        dic_autor.update(
            {'flag': 'data:image/png;base64, {0}'.format(pais['flag'])})
    else:
        dic_autor.update({'flag': ''})

    return render(request, 'biblioteca/autor.html',
                  {'autor': dic_autor, 'livros': livros})


def autores_busca(request):
    try:
        termo = request.GET.get('termo')
        if not termo:
            messages.add_message(
                request, messages.ERROR, 'Informe um valor para a busca.')
            return redirect('biblioteca:autores')

        campos = Concat('nome', Value(' '), 'pais_origem')
        autores = Autor.objects.order_by(
            'nome').distinct('nome').annotate(
                autor_pais=campos).filter(
            autor_pais__icontains=termo,
            livro__disponivel=True
        )
        if not autores or not len(autores):
            messages.add_message(
                request, messages.WARNING,
                'Nenhum autor encontrado com o termo solicitado.')
            return redirect('biblioteca:autores')

        ord = request.GET.get('ord')
        if ord and ord == '2':
            lista_ordenada = sorted(
                autores, key=operator.attrgetter('nome'), reverse=True)
        elif ord and ord == '3':
            lista_ordenada = sorted(
                autores, key=operator.methodcaller('count_livros'),
                reverse=True)
        elif ord and ord == '4':
            lista_ordenada = sorted(
                autores, key=operator.methodcaller('count_livros'))
        else:
            lista_ordenada = sorted(autores, key=operator.attrgetter('nome'))

        lista_autores = []
        for autor in lista_ordenada:  # autores:
            item = {'autor': autor}
            pais = next(filter(
                lambda x: x['pt-br'] == autor.pais_origem, countries), None)
            if pais:
                item.update(
                    {'flag': f'data:image/png;base64, {pais["flag"]}'})
            else:
                item.update({'flag': ''})
            lista_autores.append(item)
        paginator = Paginator(lista_autores, 20)
        pg = request.GET.get('pg')
        autores = paginator.get_page(pg)
        classificacoes = [
            {'id': '1', 'descricao': 'Nome de A - Z'},
            {'id': '2', 'descricao': 'Nome de Z - A'},
            {'id': '3', 'descricao': 'Mais livros'},
            {'id': '4', 'descricao': 'Menos livros'}
        ]
        return render(request, 'biblioteca/autores_busca.html',
                      {'autores': autores, 'classificacao': classificacoes})
    except Autor.DoesNotExist:
        raise Http404()
