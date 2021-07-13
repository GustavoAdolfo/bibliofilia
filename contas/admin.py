from django.contrib import admin
from .models import Perfil


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'logradouro',
                    'celular', 'related_email')
    list_filter = ('logradouro', 'bairro', 'cidade')
    list_display_links = ('user_id', 'user')
    list_per_page = 15
    search_fields = ('user', 'celular', 'logradouro',
                     'related_email', 'bairro')

    def related_email(self, obj):
        return obj.user.email
    related_email.short_description = 'Email'


admin.site.register(Perfil, PerfilAdmin)
