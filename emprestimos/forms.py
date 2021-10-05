from django import forms
from emprestimos.models import Emprestimo


class AgendamentoForm(forms.Form):
    data_agendamento = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'id': 'id_data_agendamento'
        }),
        required=True,
        label='Informe a data pretendida para devolução',
        help_text='No momento é possível escolher apenas sábados e domingos entre 10h e 17h.')
    hora_inicial = forms.CharField(
        widget=forms.NumberInput({'min': 10, 'max': 17}),
        required=False)
    hora_final = forms.CharField(
        widget=forms.NumberInput({'min': 10, 'max': 17}),
        required=False)
    emprestimo_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput())


class EmprestimoForm(forms.Form):
    data_previsao_retirada_1 = forms.DateField(
        required=True, label='Previsão de Retirada 1',  # input_formats='%m/%d/%Y',
        help_text='No momento é possível escolher apenas sábados ou domingos')
    data_previsao_retirada_2 = forms.DateField(
        required=True, label='Previsão de Retirada 1',  # input_formats='%m/%d/%Y',
        help_text='No momento é possível escolher apenas sábados ou domingos')
    observacoes = forms.CharField(
        max_length=500, label='Observações', strip=True, required=False)

    data_solicitacao = forms.CharField(widget=forms.HiddenInput())
    data_prevista_devolucao_1 = forms.CharField(widget=forms.HiddenInput())
    data_prevista_devolucao_2 = forms.CharField(widget=forms.HiddenInput())
    livro_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput())
    titulo_livro_historico = forms.CharField(widget=forms.HiddenInput())
    nome_usuario_historico = forms.CharField(widget=forms.HiddenInput())
