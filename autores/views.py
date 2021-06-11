from django.shortcuts import render, get_object_or_404
from .models import Autor


def index(request):
    autores = Autor.objects.all()
    return render(request, 'autores/index.html',
                  {'autores': autores})
    return render(request, 'autores/index.html')


def autor(request, autor_id):
    autor = get_object_or_404(Autor, id=autor_id)
    return render(request, 'autores/autor.html',
                  {'livro': autor})
