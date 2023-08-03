# Generated by Django 4.1.3 on 2023-08-01 23:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Municipe", "0004_municipe_nacionalidade"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Audiencia",
            fields=[
                (
                    "id",
                    models.AutoField(
                        db_column="id_audiencia", primary_key=True, serialize=False
                    ),
                ),
                ("data", models.DateField(db_column="data")),
                ("hora", models.TimeField(db_column="hora")),
                ("local", models.CharField(db_column="local", max_length=100)),
                ("descricao", models.CharField(db_column="descricao", max_length=100)),
                ("estado", models.CharField(db_column="estado", max_length=100)),
                (
                    "municipe",
                    models.ForeignKey(
                        db_column="id_municipe",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Municipe.municipe",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        db_column="utilizador",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "audiencia",
            },
        ),
    ]
