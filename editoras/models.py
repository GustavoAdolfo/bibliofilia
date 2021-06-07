from django.db import models
from django.db.models import base
from django.utils import timezone


class Editora(models.Model):
    nome = models.CharField(max_length=150)
    link = models.CharField(max_length=200, blank=True)
    imagem = models.CharField(max_length=500, blank=True)
    data_cadastro = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
