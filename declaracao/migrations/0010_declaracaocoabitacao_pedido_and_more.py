# Generated by Django 4.2.4 on 2023-09-18 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('declaracao', '0009_declaracaocoabitacao_bairro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaracaocoabitacao',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaocredencialviagem',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaomatricial',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaoobito',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaopobreza',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaoresidencia',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
        migrations.AddField(
            model_name='declaracaoviagem',
            name='pedido',
            field=models.FileField(null=True, upload_to='pedidos/'),
        ),
    ]
