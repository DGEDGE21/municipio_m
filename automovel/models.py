from django.db import models
from Municipe.models import Municipe
class Automovel(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_automovel')
    id_municipe = models.ForeignKey(Municipe,on_delete=models.CASCADE, null=True,db_column='id_Municipe')
    matricula = models.CharField(max_length=20, db_column='matricula', verbose_name='Matrícula')
    marca = models.CharField(max_length=100, db_column='marca')
    modelo = models.CharField(max_length=100, db_column='modelo')
    combustivel = models.CharField(max_length=50, db_column='combustivel')
    cilindrada = models.CharField(max_length=50, db_column='cilindrada')
    lotacao = models.CharField(max_length=50, db_column='lotacao')
    ano_fabrico = models.IntegerField(db_column='ano_fabrico', verbose_name='Ano de Fabrico')
    ano_compra = models.IntegerField(db_column='ano_compra', verbose_name='Ano de Compra')
    tipo = models.CharField(max_length=50, db_column='tipo')
    natureza = models.CharField(max_length=50, db_column='natureza')
    capacidade_carga = models.CharField(max_length=50, db_column='capacidade_carga')
    data_registro = models.DateTimeField(auto_now_add=True, db_column='data_registro', verbose_name='Data de Registro')

    
    class Meta:
        db_table = 'automovel'

    def __str__(self):
        return self.matricula
    
class Automovel_Grupo(models.Model):
    idGrupo=models.BigAutoField(primary_key=True)
    grupo = models.CharField(null=False, max_length=50,default='ola')
    cilindara_inicialg = models.CharField(null=False, max_length=50 ,default='ola')
    cilindara_finalg = models.CharField(null=False, max_length=50,default='ola')
    cilindara_inicialdi = models.CharField(null=False, max_length=50,default='ola')
    cilindara_finaldi = models.CharField(null=False, max_length=50,default='ola')
    cilindara_inicialvol = models.CharField(null=False, max_length=50,default='ola')
    cilindara_finaldvol = models.CharField(null=False, max_length=50,default='ola')

    def __str__(self) -> str:
        return f'{self.grupo}-{self.cilindara_finalg},{self.cilindara_finalg},{self.grupo}'

class Automovel_Grupo_Escalao(models.Model):
    idEscalao = models.BigAutoField(primary_key=True)
    primeiro_escalao = models.CharField(null=False, max_length=50,default='ola')
    segundo_escalao = models.CharField(null=False, max_length=50,default='ola')
    Terceiro_escalao = models.CharField(null=False, max_length=50,default='ola')
    grupo = models.ForeignKey(Automovel_Grupo, null=True, on_delete=models.SET_NULL)
    def __str__(self) -> str:
        return f'{self.primeiro_escalao}-{self.segundo_escalao},{self.Terceiro_escalao},{self.grupo}'
