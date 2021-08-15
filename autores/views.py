from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Autor
from livros.models import Livro
import json
from django.contrib.staticfiles.storage import staticfiles_storage
import operator
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Value
from django.db.models.functions import Concat


url = staticfiles_storage.path('data/countries.json')
countries = []
try:
    with open(url, "r") as cdata:
        content = ''.join(cdata.readlines())
        countries = json.loads(content)
        countries = list(filter(lambda x: 'pt-br' in x, countries))
except Exception as ex:
    pass


def index(request):
    ord = request.GET.get('ord')
    autores = Autor.objects.order_by('nome').filter(
        livro__disponivel=True).distinct('nome')
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
    return render(request, 'autores/index.html',
                  {'autores': autores, 'classificacao': classificacoes})


def autor(request, aid):
    autor = get_object_or_404(Autor, id=aid)
    livros = autor.livro_set.filter(autor_id=aid,
                                    disponivel=True)
    dic_autor = {'autor': autor}
    pais = next(filter(
        lambda x: x['pt-br'] == autor.pais_origem, countries), None)
    if pais:
        dic_autor.update(
            {'flag': 'data:image/png;base64, {0}'.format(pais['flag'])})
    else:
        dic_autor.update({'flag': ''})

    return render(request, 'autores/autor.html',
                  {'autor': dic_autor, 'livros': livros})


def busca(request):
    try:
        termo = request.GET.get('termo')
        if not termo:
            messages.add_message(
                request, messages.ERROR, 'Informe um valor para a busca.')
            return redirect('autores')

        campos = Concat('nome', Value(' '), 'pais_origem')
        autores = Autor.objects.order_by('nome').distinct('nome').annotate(
            autor_pais=campos
        ).filter(
            autor_pais__icontains=termo,
            livro__disponivel=True
        )
        if not autores or not len(autores):
            messages.add_message(
                request, messages.WARNING,
                'Nenhum autor encontrado com o termo solicitado.')
            return redirect('autores')

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
        return render(request, 'autores/index.html',
                      {'autores': autores, 'classificacao': classificacoes})
    except Autor.DoesNotExist:
        raise Http404()
