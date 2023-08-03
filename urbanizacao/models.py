from django.db import models
from datetime import date
from pagamentos.models import UrbPagamento
from django.contrib.auth.models import User

class LicensaBase(models.Model):
    id = models.AutoField(primary_key=True)  # Chave primária autoincrementada
    nome = models.CharField(max_length=100)
    data_nasc = models.CharField(null=True,max_length=100)
    naturalidade = models.CharField(max_length=100)
    bi = models.CharField(null=True,max_length=100)
    bi_emissao = models.CharField(max_length=100)
    bi_local = models.CharField(max_length=100)
    pagamento =models.OneToOneField(UrbPagamento, on_delete=models.CASCADE, db_column='id_pagamento_urbanizacao')
    status = models.CharField(max_length=100, default="Aguardando Aprovacao")
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE, db_column='user_id')
    class Meta:
        abstract = True

class LicensaDuat(LicensaBase):
    bairro = models.CharField(null=True, max_length=100)
    quarteirao = models.CharField(null=True, max_length=100)
    area= models.CharField(null=True, max_length=100)
    data_atribuicao= models.CharField(null=True, max_length=100)

class LicensaConstrucao(LicensaBase):
    bairro = models.CharField(null=True, max_length=100)
    quarteirao = models.CharField(null=True, max_length=100)
    finalidade = models.CharField(max_length=100)
    area_lougradouro = models.CharField(max_length=100)
    area_construcao = models.CharField(max_length=100)
    nr_pisos = models.IntegerField()
    destino_obra = models.CharField(max_length=100)
    valor_obra = models.DecimalField(max_digits=10, decimal_places=2)
    regime_obra = models.CharField(max_length=100)
    responsavel_obra = models.CharField(max_length=100)
    responsavel_nr = models.CharField(max_length=100)
