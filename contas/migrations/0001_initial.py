# Generated by Django 3.2.3 on 2021-07-13 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('celular', models.PositiveIntegerField()),
                ('cep', models.PositiveIntegerField()),
                ('logradouro', models.CharField(max_length=50)),
                ('numero', models.CharField(blank=True, max_length=10)),
                ('complemento', models.CharField(blank=True, max_length=50)),
                ('bairro', models.CharField(max_length=150)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(default='SP', max_length=2)),
                ('url_foto', models.CharField(blank=True, max_length=300)),
                ('data_cadastro', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_alteracao', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_aceite_termos', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
