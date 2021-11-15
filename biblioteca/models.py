from django.db import models
from django.utils import timezone


class Editora(models.Model):
    nome = models.CharField(max_length=150)
    link = models.CharField(max_length=200, blank=True)
    imagem = models.CharField(max_length=500, blank=True)
    data_cadastro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'editoras'
        verbose_name = 'editora'

    def __str__(self):
        return self.nome


class Autor(models.Model):
    nome = models.CharField(max_length=150)
    imagem = models.CharField(max_length=500, blank=True)
    url_wiki = models.CharField(max_length=500, blank=True)
    pais_origem = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'autores'
        verbose_name = 'autor'

    def __str__(self):
        return self.nome

    def count_livros(self):
        return self.livro_set.filter(disponivel=True).count()


class Livro(models.Model):
    titulo = models.CharField(max_length=150)
    subtitulo = models.CharField(max_length=150, blank=True)
    idioma = models.CharField(max_length=30, default='Português')
    disponivel = models.BooleanField(default=False)
    emprestado = models.BooleanField(default=False)
    sinopse = models.CharField(max_length=2000, blank=True)
    link_amazon = models.CharField(max_length=500, blank=True)
    capa = models.CharField(max_length=500, blank=True)
    autor = models.ForeignKey(Autor, on_delete=models.DO_NOTHING, default=1)
    editora = models.ForeignKey(Editora, on_delete=models.DO_NOTHING)
    data_cadastro = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'livros'
        verbose_name = 'livro'

    def __str__(self):
        if self.subtitulo:
            return self.titulo + ' - ' + self.subtitulo
        else:
            return self.titulo
