# Generated by Django 5.1.6 on 2025-02-25 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negocios', '0005_categoria_imagem_categoria_slug_estabelecimento_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estabelecimento',
            old_name='redes_sociais',
            new_name='facebook',
        ),
        migrations.RemoveField(
            model_name='estabelecimento',
            name='categoria',
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='categorias',
            field=models.ManyToManyField(to='negocios.categoria'),
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='linkedin',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='tiktok',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='estabelecimento',
            name='youtube',
            field=models.URLField(blank=True, null=True),
        ),
    ]
