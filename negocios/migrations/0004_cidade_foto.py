# Generated by Django 5.1.6 on 2025-02-23 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negocios', '0003_alter_estabelecimento_descricao'),
    ]

    operations = [
        migrations.AddField(
            model_name='cidade',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='cidades/'),
        ),
    ]
