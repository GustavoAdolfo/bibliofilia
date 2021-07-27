from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from .models import Autor
from livros.models import Livro
import json
from django.contrib.staticfiles.storage import staticfiles_storage


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
    autores = Autor.objects.order_by('nome').filter(
        livro__disponivel=True).distinct('nome')
    lista_autores = []
    for autor in autores:
        dic_autor = {'autor': autor}
        pais = next(filter(
            lambda x: x['pt-br'] == autor.pais_origem, countries), None)
        if pais:
            dic_autor.update(
                {'flag': 'data:image/png;base64, {0}'.format(pais['flag'])})
        else:
            dic_autor.update({'flag': ''})
        lista_autores.append(dic_autor)
    return render(request, 'autores/index.html',
                  {'autores': lista_autores})


def autor(request, aid):
    autor = get_object_or_404(Autor, id=aid)
    livros = autor.livro_set.filter(autor_id=aid,
                                    disponivel=True)
    return render(request, 'autores/autor.html',
                  {'autor': autor, 'livros': livros})
