from django.contrib import admin
from .models import Autor


class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'pais_origem', 'url_wiki')
    list_filter = ('pais_origem',)
    list_display_links = ('id', 'nome')
    list_per_page = 15
    search_fields = ('nome', 'pais_origem')


admin.site.register(Autor, AutorAdmin)
