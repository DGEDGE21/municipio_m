from django.db import models
from datetime import date
from pagamentos.models import DeclaracaoPagamento
from django.contrib.auth.models import User

class DeclaracaoBase(models.Model):
    id = models.AutoField(primary_key=True)  # Chave primária autoincrementada
    nome = models.CharField(max_length=100)
    estado_civil = models.CharField(null=True, default='Solteiro', max_length=100)
    bairro = models.CharField(null=True, default='Nhocane',max_length=100)
    data_nasc = models.CharField(null=True,max_length=100)
    pai = models.CharField(max_length=100)
    mae = models.CharField(max_length=100)
    naturalidade = models.CharField(max_length=100)
    bi = models.CharField(null=True,max_length=100)
    bi_emissao = models.CharField(max_length=100)
    bi_local = models.CharField(max_length=100)
    pagamento =models.OneToOneField(DeclaracaoPagamento, on_delete=models.CASCADE, db_column='id_pagamento_declaracao')
    status = models.CharField(max_length=100, default="Aguardando Aprovacao")
    data_registo = models.DateTimeField(auto_now_add=True, null=True)
    data_aprovacao = models.DateTimeField(null=True)
    user = models.ForeignKey(User, null=True,on_delete=models.CASCADE, db_column='user_id')
    class Meta:
        abstract = True

class DeclaracaoCoabitacao(DeclaracaoBase):
    conjo = models.CharField(max_length=100)
    tempo_residencia = models.CharField(max_length=100)

class DeclaracaoPobreza(DeclaracaoBase):
    razao = models.CharField(max_length=100)
    tempo_residencia = models.CharField(max_length=100)

class DeclaracaoResidencia(DeclaracaoBase):
    razao = models.CharField(max_length=100)
    tempo_residencia = models.CharField(max_length=100)

class DeclaracaoMatricial(DeclaracaoBase):
    pass  # Não possui campos adicionais além dos campos herdados

class DeclaracaoViagem(DeclaracaoBase):
    nome_menor = models.CharField(max_length=100)
    relacao_menor = models.CharField(max_length=100)
    razao = models.CharField(max_length=100)
    tempo_residencia = models.CharField(max_length=100)


class DeclaracaoCredencialViagem(DeclaracaoBase):
    veiculo_marca = models.CharField(max_length=100)
    veiculo_matricula = models.CharField(max_length=100)
    lotacao = models.PositiveIntegerField()
    validade = models.DateField()

class DeclaracaoObito(DeclaracaoBase):
    data_obito = models.DateField()
    razao_obito = models.CharField(max_length=100)


