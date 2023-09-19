from django.db import models
from datetime import date
from pagamentos.models import DeclaracaoPagamento
from django.contrib.auth.models import User

class DeclaracaoBase(models.Model):
    id = models.AutoField(primary_key=True)  # Chave primária autoincrementada
    nome = models.CharField(max_length=100, null=True)
    estado_civil = models.CharField(null=True, default='Solteiro', max_length=100)
    bairro = models.CharField(null=True, default='Nhocane',max_length=100)
    data_nasc = models.CharField(null=True,max_length=100)
    pai = models.CharField(max_length=100, null=True)
    mae = models.CharField(max_length=100, null=True)
    naturalidade = models.CharField(max_length=100, null=True)
    bi = models.CharField(null=True,max_length=100)
    bi_emissao = models.CharField(max_length=100, null=True)
    bi_local = models.CharField(max_length=100, null=True)
    pagamento =models.OneToOneField(DeclaracaoPagamento, on_delete=models.CASCADE, db_column='id_pagamento_declaracao')
    status = models.CharField(max_length=100, default="Aguardando Aprovacao", null=True)
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE, db_column='user_id')
    pedido = models.FileField(upload_to='pedidos/', null=True)
    class Meta:
        abstract = True

class DeclaracaoCoabitacao(DeclaracaoBase):
    conjo = models.CharField(max_length=100, null=True)
    tempo_residencia = models.CharField(max_length=100, null=True)

class DeclaracaoPobreza(DeclaracaoBase):
    razao = models.CharField(max_length=100, null=True)
    tempo_residencia = models.CharField(max_length=100, null=True)

class DeclaracaoResidencia(DeclaracaoBase):
    razao = models.CharField(max_length=100, null=True)
    tempo_residencia = models.CharField(max_length=100, null=True)

class DeclaracaoMatricial(DeclaracaoBase):
    pass  # Não possui campos adicionais além dos campos herdados

class DeclaracaoViagem(DeclaracaoBase):
    nome_menor = models.CharField(max_length=100, null=True)
    relacao_menor = models.CharField(max_length=100, null=True)
    razao = models.CharField(max_length=100, null=True)
    tempo_residencia = models.CharField(max_length=100, null=True)


class DeclaracaoCredencialViagem(DeclaracaoBase):
    veiculo_marca = models.CharField(max_length=100, null=True)
    veiculo_matricula = models.CharField(max_length=100, null=True)
    lotacao = models.PositiveIntegerField(null=True)
    validade = models.DateField(null=True)

class DeclaracaoObito(DeclaracaoBase):
    data_obito = models.DateField(null=True)
    razao_obito = models.CharField(max_length=100, null=True)


