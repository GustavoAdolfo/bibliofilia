from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    celular = models.PositiveBigIntegerField()
    cep = models.PositiveIntegerField()
    logradouro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=150)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='SP')
    url_foto = models.ImageField(
        blank=True, null=True, upload_to='fotos/%Y/%m/')
    data_cadastro = models.DateTimeField(default=timezone.now)
    data_alteracao = models.DateTimeField(default=timezone.now)
    data_aceite_termos = models.DateTimeField(default=timezone.now)
    permitir_emprestimo = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.celular
