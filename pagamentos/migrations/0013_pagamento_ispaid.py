# Generated by Django 4.2.4 on 2023-09-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamentos', '0012_genericopagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='isPaid',
            field=models.BooleanField(db_column='status', default=True),
        ),
    ]
