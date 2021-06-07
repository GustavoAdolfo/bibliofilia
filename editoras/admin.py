from django.contrib import admin
from .models import Editora


class EditoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'link')
    list_display_links = ('id', 'nome')
    list_per_page = 15
    search_fields = ('nome',)


admin.site.register(Editora, EditoraAdmin)
