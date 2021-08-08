from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from .models import Autor
from livros.models import Livro
import json
from django.contrib.staticfiles.storage import staticfiles_storage
import operator
from django.core.paginator import Paginator


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
    return render(request, 'autores/index.html',
                  {'autores': autores})


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
