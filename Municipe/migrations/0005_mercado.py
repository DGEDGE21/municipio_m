# Generated by Django 4.1.3 on 2023-08-07 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Municipe", "0004_municipe_nacionalidade"),
    ]

    operations = [
        migrations.CreateModel(
            name="Mercado",
            fields=[
                (
                    "id",
                    models.AutoField(
                        db_column="id_mercado", primary_key=True, serialize=False
                    ),
                ),
                (
                    "nome",
                    models.CharField(
                        db_column="nome_mercado",
                        max_length=100,
                        verbose_name="Nome do Mercado",
                    ),
                ),
            ],
            options={
                "db_table": "mercado",
            },
        ),
    ]
