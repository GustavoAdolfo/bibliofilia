from django.shortcuts import render
from .models import Livro


def index(request):
    livros = Livro.objects.all()
    return render(request, 'livros/index.html',
                  {'livros': livros})


def livro(request, lvid):
    livro = Livro.objects.get(id=lvid)
    return render(request, 'livros/livro.html',
                  {'livro': livro})
