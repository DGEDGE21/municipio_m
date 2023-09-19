from django.db import models
from datetime import date
from pagamentos.models import TransPagamento
from django.contrib.auth.models import User
from automovel.models import Automovel

class LicensaTransporte(models.Model):
    id = models.AutoField(primary_key=True)
    veiculo = models.ForeignKey(Automovel, null=True, on_delete=models.CASCADE, db_column='id_automovel')
    rota = models.CharField(null=True, max_length=100)
    pagamento =models.OneToOneField(TransPagamento, on_delete=models.CASCADE, db_column='id_pagamento_transporte')
    status = models.CharField(max_length=100, default="Aguardando Aprovacao")
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE, db_column='user_id')
    pedido = models.FileField(upload_to='pedidos/', null=True)

class LicensaAgua(models.Model):
    id = models.AutoField(primary_key=True)
    pagamento = models.OneToOneField(TransPagamento, on_delete=models.CASCADE, db_column='id_pagamento_transporte')
    bairro= models.CharField(max_length=100, null=True)
    quarteirao=models.CharField(max_length=100, null=True)
    nr_casa= models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, default="Aguardando Aprovacao")
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_column='user_id')
    pedido = models.FileField(upload_to='pedidos/', null=True)