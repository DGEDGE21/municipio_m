# Generated by Django 4.2.4 on 2023-09-16 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('audiencia', '0002_audiencia_data_registo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiencia',
            name='user',
            field=models.ForeignKey(db_column='utilizador', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
