from django.db import models
from django.contrib.auth.models import User
from Municipe.models import Municipe

# Create your models here.
#cria um model chamado vereacao com id e nome
class Unidade(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_unidade')
    nome = models.CharField(max_length=100, db_column='nome')

    def __str__(self):
        return f"{self.id}-{self.nome}"

    class Meta:
        db_table = 'unidade'

#cria um model chamado funcionario com id, municipe, vereacao e cargo
class Funcionario(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_funcionario')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, db_column='id_unidade')
    cargo = models.CharField(max_length=100, db_column='cargo')
    user = models.OneToOneField(User,null=True,  on_delete=models.CASCADE, db_column="utilizador")
    isActive = models.BooleanField(default=True, db_column='isActive')
    def __str__(self):
        return f"{self.unidade.nome} - {self.municipe.nome} - {self.cargo}"

    class Meta:
        db_table = 'funcionario'