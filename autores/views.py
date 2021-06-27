from django.shortcuts import render, get_object_or_404
from .models import Autor
from livros.models import Livro


def index(request):
    autores = Autor.objects.order_by('nome').filter(
        livro__disponivel=True).distinct('nome')
    return render(request, 'autores/index.html',
                  {'autores': autores})


def autor(request, aid):
    autor = get_object_or_404(Autor, id=aid)
    livros = autor.livro_set.filter(autor_id=aid,
                                    disponivel=True)
    return render(request, 'autores/autor.html',
                  {'autor': autor, 'livros': livros})
