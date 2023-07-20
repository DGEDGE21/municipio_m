# Generated by Django 4.1.3 on 2023-07-18 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Municipe", "0003_alter_municipe_nr_contribuente"),
    ]

    operations = [
        migrations.CreateModel(
            name="Estabelecimento",
            fields=[
                (
                    "id",
                    models.AutoField(
                        db_column="id_estabelecimento",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("sector", models.CharField(db_column="sector", max_length=100)),
                ("area", models.CharField(db_column="area", max_length=20)),
                (
                    "valor_tae",
                    models.DecimalField(
                        db_column="valor_tae", decimal_places=2, max_digits=10
                    ),
                ),
                (
                    "data_registro",
                    models.DateTimeField(
                        auto_now_add=True,
                        db_column="data_registro",
                        verbose_name="Data de Registro",
                    ),
                ),
                (
                    "bairro",
                    models.ForeignKey(
                        db_column="bairro_id",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Municipe.bairro",
                        verbose_name="Bairro",
                    ),
                ),
                (
                    "id_municipe",
                    models.ForeignKey(
                        db_column="id_Municipe",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Municipe.municipe",
                    ),
                ),
            ],
            options={
                "db_table": "estabelecimento",
            },
        ),
    ]
