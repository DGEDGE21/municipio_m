# Generated by Django 4.2.4 on 2023-08-17 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenciamento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='licensaae',
            name='destino',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
