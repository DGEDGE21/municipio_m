from django.db import models
from pagamentos.models import GenericoPagamento
from django.contrib.auth.models import User

# Licensa por activades economicas
class LicensaAE(models.Model):
    id = models.AutoField(primary_key=True)
    pagamento = models.OneToOneField(GenericoPagamento, on_delete=models.CASCADE, db_column='id_pagamento_generico')
    destino = models.CharField(max_length=100, null=True)
    bairro= models.CharField(max_length=100, null=True)
    quarteirao=models.CharField(max_length=100, null=True)
    nr_casa= models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, default="Aguardando Aprovacao")
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_column='user_id')