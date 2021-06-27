from django.db import models
# from livros.models import Livro


class Autor(models.Model):
    nome = models.CharField(max_length=150)
    imagem = models.CharField(max_length=500, blank=True)
    url_wiki = models.CharField(max_length=500, blank=True)
    pais_origem = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nome

    def count_livros(self):
        return self.livro_set.filter(disponivel=True).count()
