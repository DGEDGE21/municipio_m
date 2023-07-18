# Generated by Django 4.1.3 on 2023-07-16 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Municipe", "0003_alter_municipe_nr_contribuente"),
        ("Propriedade", "0002_alter_propriedade_bairro"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propriedade",
            name="bairro",
            field=models.ForeignKey(
                db_column="bairro_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="Municipe.bairro",
                verbose_name="Bairro",
            ),
        ),
    ]
