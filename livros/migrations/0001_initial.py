# Generated by Django 3.2.3 on 2021-07-13 00:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('editoras', '0001_initial'),
        ('autores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('subtitulo', models.CharField(blank=True, max_length=150)),
                ('idioma', models.CharField(default='Português', max_length=30)),
                ('disponivel', models.BooleanField(default=False)),
                ('sinopse', models.CharField(blank=True, max_length=2000)),
                ('link_amazon', models.CharField(blank=True, max_length=500)),
                ('capa', models.CharField(blank=True, max_length=500)),
                ('data_cadastro', models.DateTimeField(default=django.utils.timezone.now)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autores.autor')),
                ('editora', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='editoras.editora')),
            ],
        ),
    ]
