from django.shortcuts import render, redirect
from django.http import Http404
from .models import Livro
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    livros = Livro.objects.order_by('titulo').filter(disponivel=True)
    paginator = Paginator(livros, 12)
    pg = request.GET.get('pg')
    livros = paginator.get_page(pg)
    return render(request, 'livros/index.html',
                  {'livros': livros})


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

        campos = Concat('titulo', Value(' '), 'subtitulo')
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

        paginator = Paginator(livros, 10)
        pg = request.GET.get('pg')
        livros = paginator.get_page(pg)
        return render(request, 'livros/busca.html', {'livros': livros})
    except Livro.DoesNotExist:
        raise Http404()
