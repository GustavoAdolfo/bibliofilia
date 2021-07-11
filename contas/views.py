from django.shortcuts import render, get_object_or_404
from .models import Conta
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User


def index(request):
    return render(request, 'contas/index.html')


def perfil(request, id):
    # conta = get_object_or_404(Conta, id=id)
    # return render(request, 'contas/perfil.html',
    #               {'conta': conta})
    return render(request, 'contas/perfil.html')


def login(request):
    return render(request, 'contas/login.html')


def logout(request):
    return render(request, 'contas/logout.html')


def painel(request):
    return render(request, 'contas/painel.html')


def cadastro(request):
    if request.method != 'POST':
        return render(request, 'contas/index.html')

    nome = request.POST.get("nome")
    email = request.POST.get("email")
    celular = request.POST.get("celular")
    cep = request.POST.get("cep")
    logradouro = request.POST.get("logradouro")
    numero = request.POST.get("numero")
    complemento = request.POST.get("complemento")
    bairro = request.POST.get("bairro")
    cidade = request.POST.get("cidade")
    estado = request.POST.get("estado")
    foto_perfil = request.POST.get("foto-perfil")
    senha = request.POST.get("senha")
    confirmar_senha = request.POST.get("confirma-senha")
    aceite_termos = request.POST.get("aceite-termos")

    campos_invalidos = []
    if not nome or len(nome) < 9:
        campos_invalidos.append('O campo NOME está inválido!')
    if not cep or len(cep) != 8:
        campos_invalidos.append('O campo CEP está inválido!')
    if not logradouro or len(logradouro) < 5:
        campos_invalidos.append('O campo LOGRADOURO está inválido!')
    if not bairro or len(bairro) < 5:
        campos_invalidos.append('O campo BAIRRO está inválido!')
    if not cidade or len(cidade) < 3:
        campos_invalidos.append('O campo CIDADE está inválido!')
    if not estado or len(estado) < 2:
        campos_invalidos.append('O campo ESTADO está inválido!')
    if not celular or len(celular) < 11:
        campos_invalidos.append('O campo CELULAR está inválido!')
    if not senha or len(senha) < 8:
        campos_invalidos.append('O campo SENHA está inválido!')
    if not confirmar_senha or len(confirmar_senha) < 8:
        campos_invalidos.append(
            'O campo CONFIRMAÇÃO DE SENHA está inválido!')
    if confirmar_senha != senha:
        campos_invalidos.append(
            'A SENHA e a CONFIRMAÇÃO DE SENHA divergem!')
    try:
        validate_email(email)
        if User.objects.filter(email=email).exists():
            campos_invalidos.append(
                'O E-MAIL informado já está sendo utilizado!')
    except:
        campos_invalidos.append('O campo E-MAIL está inválido!')

    if not aceite_termos:
        campos_invalidos.append(
            'Você precisa estar ciente e aceitar os termos de uso e'
            ' a política de privacidade para prosseguir')

    if len(campos_invalidos):
        erros = 'Alugns campos precisam de revisão:'
        messages.error(request, erros)
        return render(request, 'contas/index.html',
                      {'erros': campos_invalidos})

    return render(request, 'contas/cadastro.html')
