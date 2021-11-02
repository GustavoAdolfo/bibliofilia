from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login
# from django.contrib.auth.forms import UserCreationForm
# from .forms import UserCreationForm
from users.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from users.models import CustomUser, Perfil
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.messages.constants import ERROR
from django.contrib import messages, auth
from django.core.validators import validate_email


def logout_view(request):
    """Faz log out do usuário."""
    logout(request)
    return HttpResponseRedirect(reverse('biblioteca:index'))


def cadastro(request):
    """Faz o cadastro de um novo usuário."""
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Faz login e redireciona para a página inicial
            # authenticated_user = authenticate(
            #     user_name=new_user.username,
            #     password=request.POST['password1'])
            # login(request, authenticated_user)
            perfil = Perfil()
            perfil.email = new_user.email
            perfil.nome = new_user.first_name
            perfil.sobrenome = new_user.last_name
            perfil.permitir_emprestimo = True
            perfil.user = new_user
            perfil.save()
            login(request, new_user)
            return HttpResponseRedirect(reverse('biblioteca:index'))

    context = {'form': form}
    return render(request, 'users/cadastro.html', context)


@login_required(login_url='usuario/login/')
@transaction.atomic
def perfil(request):
    if request.method != 'POST':
        user = auth.get_user(request)
        perfil = get_object_or_404(Perfil, user=user)
        return render(request, 'users/perfil.html', {'perfil': perfil})
    else:
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
            if Perfil.objects.filter(email=email).exists():
                msg = 'O E-MAIL informado já está sendo utilizado! '
                msg += '<a href="/contas/recuperar-senha">Recuperar senha</a>.'
                campos_invalidos.append(msg)
        except Exception:
            campos_invalidos.append('O campo E-MAIL está inválido!')

        if not aceite_termos:
            campos_invalidos.append(
                'Você precisa estar ciente e aceitar os termos de uso e'
                ' a política de privacidade para prosseguir')

        if len(campos_invalidos):
            # erros = 'Alugns campos precisam de revisão:'
            # messages.error(request, erros, extra_tags='safe')
            for erro in campos_invalidos:
                messages.add_message(request, ERROR, erro, extra_tags='safe')
            # , {'erros': campos_invalidos})
            return render(request, reverse('usuario:perfil'))

        Perfil.objects.create(user=auth.get_user_model(),
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


@login_required(login_url='usuairo/login/')
def editprofile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your Profile Updated"))
            return redirect('crmapp')
    else:
        form = UserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'editprofile.html', context)


@login_required(login_url='usuairo/login/')
def changepassword(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Changed",
                             extra_tags='green')
            return redirect('crmapp')
    else:
        form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'changepassword.html', context)
