from django.shortcuts import render
from django.http import Http404
from .models import Livro
from django.core.paginator import Paginator


def index(request):
    livros = Livro.objects.all()
    paginator = Paginator(livros, 10)
    pg = request.GET.get('pg')
    livros = paginator.get_page(pg)
    return render(request, 'livros/index.html',
                  {'livros': livros})


def livro(request, lvid):
    try:
        livro = Livro.objects.get(id=lvid)
        links = livro.link_amazon.split('|')
        return render(request, 'livros/livro.html',
                      {'livro': livro, 'links': links})
    except Livro.DoesNotExist:
        raise Http404()
