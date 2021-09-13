from django.contrib import admin
from .models import Editora, Autor, Livro


class EditoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'link')
    list_display_links = ('id', 'nome')
    list_per_page = 15
    search_fields = ('nome',)


admin.site.register(Editora, EditoraAdmin)


class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'pais_origem', 'url_wiki')
    list_filter = ('pais_origem',)
    list_display_links = ('id', 'nome')
    list_per_page = 15
    search_fields = ('nome', 'pais_origem')


admin.site.register(Autor, AutorAdmin)


class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'subtitulo', 'idioma',
                    'autor', 'editora', 'disponivel', 'emprestado')
    list_filter = ('autor', 'editora', 'idioma')
    list_display_links = ('id', 'titulo')
    list_per_page = 15
    search_fields = ('titulo', 'subtitulo', 'autor', 'editora')
    list_editable = ('disponivel', 'emprestado')


admin.site.register(Livro, LivroAdmin)
