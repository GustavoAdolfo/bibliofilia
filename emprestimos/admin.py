from django.contrib import admin
from emprestimos.models import AgendamentoDevolucao, Emprestimo


class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'livro', 'data_efetiva_emprestimo',
                    'data_efetiva_devolucao', 'data_cancelamento')
    list_display_links = ('id',)
    list_per_page = 15
    search_fields = ('user', 'livro',)


admin.site.register(Emprestimo, EmprestimoAdmin)


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'emprestimo',
                    'data_agendamento', 'hora_inicial', 'hora_final')
    list_display_links = ('id',)
    list_per_page = 15
    search_fields = ('user', 'emprestimo')


admin.site.register(AgendamentoDevolucao, AgendamentoAdmin)
