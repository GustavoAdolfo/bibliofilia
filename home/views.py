from django.shortcuts import render
from autores.models import Autor
from livros.models import Livro
from django.contrib import messages


def index(request):
    num_autores = Autor.objects.all().filter(
        livro__disponivel=True).distinct('nome').count()
    num_livros = Livro.objects.filter(disponivel=True).count()
    return render(request, 'home/index.html',
                  {'num_livros': num_livros, 'num_autores': num_autores})


def sobre(request):
    return render(request, 'home/sobre.html')
