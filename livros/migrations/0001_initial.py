# Generated by Django 3.2.3 on 2021-06-06 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('subtitulo', models.CharField(max_length=150)),
                ('editora', models.CharField(max_length=100)),
                ('capa', models.CharField(max_length=500)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autores.autor')),
            ],
        ),
    ]
