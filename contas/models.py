from django.db import models
from django.utils import timezone


class Conta(models.Model):
    nome = models.CharField(max_length=250)
    email = models.CharField(max_length=500)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=50, blank=True),
    bairro = models.CharField(max_length=150),
    cidade = models.CharField(max_length=100),
    estado = models.CharField(max_length=2),
    url_foto = models.CharField(max_length=300),
    celular = models.IntegerField(),
    senha = models.CharField(max_length=250),
    data_cadastro = models.DateTimeField(default=timezone.utc),
    data_alteracao = models.DateTimeField(default=timezone.utc),
    data_aceite_termos = models.DateTimeField(default=timezone.utc)

    def __str__(self):
        return self.nome
