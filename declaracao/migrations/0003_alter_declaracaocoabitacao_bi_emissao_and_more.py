# Generated by Django 4.1.3 on 2023-07-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("declaracao", "0002_alter_declaracaocoabitacao_pagamento_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaracaocoabitacao",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaocredencialviagem",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaomatricial",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaoobito",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaopobreza",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaoresidencia",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="declaracaoviagem",
            name="bi_emissao",
            field=models.CharField(max_length=100),
        ),
    ]
