from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages, auth
from django.contrib.messages.constants import ERROR
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views import View
from users.models import CustomUser, Perfil
import base64
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login
from django.contrib.auth.tokens import default_token_generator
from users.forms import PerfilForm, CustomUserCreationForm, \
    CustomUserChangeForm, PasswordChangeForm, PerfilForm
from users.tokens import account_activation_token
from django.utils.encoding import force_text


def logout_view(request):
    """Faz log out do usuário."""
    logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse('biblioteca:index'))


def cadastro(request):
    """Faz o cadastro de um novo usuário."""
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            Perfil.objects.create(
                nome=new_user.first_name,
                sobrenome=new_user.last_name,
                permitir_emprestimo=False,
                user=new_user
            )

            # login(request, new_user)
            messages.add_message(
                request,
                messages.WARNING,
                'Você só poderá solicitar empréstimos após completar seu ' +
                'perfil e ter seu cadastro aprovado.')
            # return HttpResponseRedirect(reverse('biblioteca:livros'))

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            new_user.email_user(subject, message)

            messages.success(
                request, ('Enviamos um e-mail para que você confirme sua conta.'))

            return HttpResponseRedirect(reverse('user:login'))

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
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your Profile Updated"))
            return redirect('crmapp')
    else:
        form = CustomUserChangeForm(instance=request.user)
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


class ChangePasswordView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'user': user}
        return render(request, 'users/changepassword.html', context)

    def post(self, request, *args, **kwargs):
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Você precisa fazer login novamente para validar a nova senha.")
            return HttpResponseRedirect(reverse('user:logout'))
        else:
            ctx = {}
            ctx['form'] = form
            return render(request, 'users/changepassword.html', ctx)


class ActivateAccountView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(
                user,
                token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            perfil = Perfil.objects.get(user_id=user.id)
            perfil.permitir_emprestimo = True
            perfil.save()
            login(request, user)
            messages.success(request, (
                'Obrigado por confirmar sua conta. Aproveite a Minhoteca!'))
            return HttpResponseRedirect(reverse('biblioteca:livros'))
        else:
            messages.warning(
                request, (
                    'O link de confirmação é inválido, possivelmente ' +
                    'porque ele já pode ter sido utilizado.'))
            form = CustomUserCreationForm()
            context = {'form': form}
            return render(request, 'users/cadastro.html', context)
