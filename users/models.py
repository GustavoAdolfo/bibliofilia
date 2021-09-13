from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Custom user model manager where email is the unique identifiers \
    for authentication instead of usernames."""

    def create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    aceite_termos = models.BooleanField(_('Termos de Uso'), default=False)
    data_aceite_termos = models.DateTimeField(
        _('Data do Aceite'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['aceite_termos']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Perfil(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(_('email de contato'), unique=True)
    nome = models.CharField(max_length=50, blank=False)
    sobrenome = models.CharField(max_length=50, blank=False)
    celular = models.PositiveBigIntegerField()
    cep = models.PositiveIntegerField()
    logradouro = models.CharField(max_length=50)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=150)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, default='SP')
    url_foto = models.ImageField(
        blank=True, null=True, upload_to='fotos/%Y/%m/')
    data_cadastro = models.DateTimeField(default=timezone.now)
    data_alteracao = models.DateTimeField(default=timezone.now)
    permitir_emprestimo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = 'perfis'
