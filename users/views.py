from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from django.core.validators import validate_email
from django.contrib import messages, auth
from django.contrib.messages.constants import ERROR
from django.db import transaction
from django.contrib.auth.decorators import login_required
from users.models import CustomUser, Perfil
import base64
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login
from django.contrib.auth.tokens import default_token_generator
from users.forms import PerfilForm, UserCreationForm, UserChangeForm, \
    PasswordChangeForm, PerfilForm


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
            perfil = Perfil()
            perfil.email = new_user.email
            perfil.nome = new_user.first_name
            perfil.sobrenome = new_user.last_name
            perfil.permitir_emprestimo = True
            perfil.user = new_user
            perfil.save()
            login(request, new_user)
            messages.add_message(request, messages.SUCCESS,
                                 'Cadastro realizado com sucesso!')
            messages.add_message(
                request,
                messages.WARNING,
                'Você só poderá solicitar empréstimos após completar seu ' +
                'perfil e ter seu cadastro aprovado.')
            return HttpResponseRedirect(reverse('biblioteca:livros'))

    context = {'form': form}
    return render(request, 'users/cadastro.html', context)


@login_required(login_url='user/login/')
@transaction.atomic
def perfil(request):
    user = auth.get_user(request)
    if request.method != 'POST':
        try:
            perfil = get_object_or_404(Perfil, user_id=user.id)
        except Exception as e:
            perfil = Perfil()
            perfil.user = user

        form = PerfilForm(instance=perfil)
        return render(request, 'users/perfil.html', {'form': form})
    else:
        if Perfil.objects.filter(user_id=user.id).exists():
            perfil = Perfil.objects.get(user_id=user.id)
            form = PerfilForm(
                instance=perfil, data=request.POST, files=request.FILES)
            if form.is_valid():
                perfil = form.save(commit=False)
                perfil.user = user
                perfil.save()
                messages.add_message(request, messages.SUCCESS,
                                     'Perfil atualizado com sucesso!')
                return HttpResponseRedirect(reverse('biblioteca:index'))
        else:
            form = PerfilForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                # Get the current instance object to display in the template
                img_obj = form.instance
                # return render(request, 'index.html', {'form': form, 'img_obj': img_obj})
                messages.add_message(request, messages.SUCCESS,
                                     'Perfil atualizado com sucesso!')
                return HttpResponseRedirect(reverse('biblioteca:index'))

        form = PerfilForm(request.POST, request.FILES)
        return render(request, 'users/perfil.html', {'form': form})


@login_required(login_url='user/login/')
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


@login_required(login_url='user/login/')
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


def password_reset_confirm(request, uidb64=None, token=None,
                           token_generator=default_token_generator):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb64 is not None and token is not None  # checked by URLconf

    try:
        uidb64 += "=" * ((4 - len(uidb64) % 4) % 4)
        uid_int = int(base64.b64decode(uidb64))
        user = CustomUser.objects.get(id=uid_int)
    except Exception as e:
        print(e)
        user = None

    ctx = {}

    if user is not None and token_generator.check_token(user, token):
        ctx['validlink'] = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('user:password_reset_complete'))
            else:
                ctx['form'] = form
                return render(request, 'users/password_reset_confirm.html', ctx)
        else:
            form = SetPasswordForm(user, request.GET)
            ctx['form'] = form
            return render(request, 'users/password_reset_confirm.html', ctx)
    else:
        ctx['validlink'] = False
        messages.add_message(
            request, messages.ERROR, 'Este link não é mais válido. Se deseja alterar sua senha, solicite novamente.')
        return HttpResponseRedirect(reverse('user:password_reset'))
