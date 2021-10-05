from django.db import models
from users.models import CustomUser
from biblioteca.models import Livro
from django.utils import timezone
from datetime import datetime, date


class Emprestimo(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=False)
    livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING, blank=False)
    nome_usuario_historico = models.CharField(
        max_length=100, blank=True)
    titulo_livro_historico = models.CharField(
        max_length=300, blank=True)
    data_solicitacao = models.DateTimeField(default=timezone.now, blank=False)
    data_previsao_retirada_1 = models.DateField(blank=True, null=True)
    data_previsao_retirada_2 = models.DateField(blank=True, null=True)
    data_prevista_devolucao_1 = models.DateField(blank=True, null=True)
    data_prevista_devolucao_2 = models.DateField(blank=True, null=True)
    data_efetiva_emprestimo = models.DateField(blank=True, null=True)
    data_efetiva_devolucao = models.DateField(blank=True, null=True)
    cancelado = models.BooleanField(default=False)
    data_cancelamento = models.DateField(blank=True, null=True)
    observacoes = models.TextField(max_length=500, blank=True)

    def __str__(self):
        if isinstance(self.data_solicitacao, str):
            return self.livro.titulo + ' - Empréstimo solicitado em: ' + \
                datetime.fromisoformat(
                    self.data_solicitacao).strftime('%d/%m/%Y')
        elif isinstance(self.data_solicitacao, datetime):
            return self.livro.titulo + ' - Empréstimo solicitado em: ' + \
                self.data_solicitacao.strftime('%d/%m/%Y')
        else:
            return self.livro.titulo + ' - Solicitação realizada'

    def obter_agendamento(self):
        if self.agendamentodevolucao_set:
            agendamento = self.agendamentodevolucao_set.get()
            if isinstance(agendamento.data_agendamento, str):
                return datetime.fromisoformat(
                    agendamento.data_agendamento).strftime('%d/%m/%Y')
            elif isinstance(agendamento.data_agendamento, date):
                return agendamento.data_agendamento.strftime('%d/%m/%Y')
            else:
                return

    class Meta:
        verbose_name_plural = 'emprestimos'
        unique_together = ('user', 'livro', 'data_solicitacao')


class Espera(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.DO_NOTHING, blank=False)
    livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING, blank=False)
    nome_usuario_historico = models.CharField(
        max_length=100, blank=True, default=str(CustomUser))
    titulo_livro_historico = models.CharField(
        max_length=300, blank=True, default=str(Livro))
    data_solicitacao = models.DateTimeField(default=timezone.now, blank=False)
    data_previsao_emprestimo_1 = models.DateField(blank=False)
    data_previsao_emprestimo_2 = models.DateField(blank=False)
    emprestimo_efetuado = models.BooleanField(default=False)
    observacoes = models.TextField(max_length=500)

    def __str__(self):
        return self.livro.titulo + ' - Reservado em: ' + \
            str(self.data_efetiva_emprestimo)

    class Meta:
        verbose_name_plural = 'esperas'


class AgendamentoDevolucao(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.DO_NOTHING)
    data_agendamento = models.DateField(blank=False)
    hora_inicial = models.PositiveSmallIntegerField(default=10)
    hora_final = models.PositiveSmallIntegerField(default=17)

    def __str__(self):
        if isinstance(self.data_agendamento, str):
            return datetime.fromisoformat(
                self.data_agendamento).strftime('%d/%m/%Y')
        elif isinstance(self.data_agendamento, datetime):
            return self.data_agendamento.strftime('%d/%m/%Y')
        else:
            return 'Devolução não agendada'

    class Meta:
        verbose_name_plural = 'agendamentos'
        unique_together = ('user', 'emprestimo', 'data_agendamento')
