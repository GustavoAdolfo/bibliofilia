from django.db import models
from django.db.models import base
from django.utils import timezone
from autores.models import Autor
from editoras.models import Editora


class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=150, blank=True)
    idioma = models.CharField(max_length=30, default='Português')
    disponivel = models.BooleanField(default=False)
    sinopse = models.CharField(max_length=2000, blank=True)
    link_amazon = models.CharField(max_length=500, blank=True)
    capa = models.CharField(max_length=500, blank=True)
    autor = models.ForeignKey(Autor, on_delete=models.DO_NOTHING)
    editora = models.ForeignKey(Editora, on_delete=models.DO_NOTHING)
    data_cadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
