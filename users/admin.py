from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Perfil


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',
                    'aceite_termos', 'data_aceite_termos')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
         'aceite_termos', 'data_aceite_termos')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'email', 'password1', 'password2', 'is_staff', 'is_active')}),)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user', 'logradouro',
                    'celular')
    list_filter = ('logradouro', 'bairro', 'cidade')
    list_display_links = ('user_id', 'user')
    list_per_page = 15
    search_fields = ('user', 'celular', 'logradouro',
                     'email', 'bairro')


admin.site.register(Perfil, PerfilAdmin)
