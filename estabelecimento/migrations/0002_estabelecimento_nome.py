# Generated by Django 4.1.3 on 2023-07-18 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("estabelecimento", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="estabelecimento",
            name="nome",
            field=models.CharField(db_column="nome", max_length=100, null=True),
        ),
    ]
