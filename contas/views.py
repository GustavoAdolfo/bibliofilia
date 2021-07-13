from django.shortcuts import render, get_object_or_404, redirect
from .models import Perfil
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from .models import Perfil
from django.db import transaction
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'contas/index.html')


@login_required(login_url='/contas')
def perfil(request, id):
    # conta = get_object_or_404(Conta, id=id)
    # return render(request, 'contas/perfil.html',
    #               {'conta': conta})
    return render(request, 'contas/perfil.html')


def login(request):
    if request.method != 'POST':
        return render(request, 'contas/index.html')

    username = request.POST.get('email')
    password = request.POST.get('senha')

    user = auth.authenticate(request, username=username, password=password)
    if not user:
        messages.error(request, "E-mail ou senha inválidos!")
        return render(request, 'contas/index.html')

    auth.login(request, user)
    messages.success(request, 'Bem vindo {}!'.format(user.first_name))
    return redirect('/')


def logout(request):
    auth.logout(request)
    messages.success(request, 'Você saiu da sua conta.')
    return redirect('index')


@login_required(login_url='/contas')
def painel(request):
    return render(request, 'contas/painel.html')


def cadastro(request):
    return render(request, 'contas/cadastro.html')


@transaction.atomic
def registrar(request):
    if request.method != 'POST':
        return render(request, 'contas/index.html')

    nome = request.POST.get("nome")
    sobrenome = request.POST.get("sobrenome")
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
    if not nome or len(nome) < 3:
        campos_invalidos.append('O campo NOME está inválido!')
    if not sobrenome or len(sobrenome) < 3:
        campos_invalidos.append('O campo SOBRENOME está inválido!')
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

    user = User.objects.create(
        username=email,
        email=email,
        first_name=nome,
        last_name=sobrenome)
    user.set_password(senha)
    user.save()
    Perfil.objects.create(user=user,
                          celular=celular,
                          cep=cep,
                          logradouro=logradouro,
                          numero=numero,
                          complemento=complemento,
                          bairro=bairro,
                          cidade=cidade,
                          estado=estado,
                          url_foto=foto_perfil  # SUBIR O ARQUIVO PARA ALGUM LUGAR E ENTÃO PASSAR A URL
                          )
    return render(request, 'contas/index.html', {'novo_cadastro': True})
