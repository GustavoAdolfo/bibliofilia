# Generated by Django 3.2.3 on 2021-06-07 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0003_alter_livro_editora'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='idioma',
            field=models.CharField(default='Português', max_length=30),
        ),
    ]
