from django.db import models
from Municipe.models import Municipe, Bairro

class Estabelecimento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_estabelecimento')
    id_municipe = models.ForeignKey(Municipe,on_delete=models.CASCADE, db_column='id_Municipe')
    nome = models.CharField(max_length=100, null=True,db_column='nome')
    sector = models.CharField(max_length=100, db_column='sector')
    area = models.CharField(max_length=20, db_column='area')
    bairro = models.ForeignKey(Bairro, null=True,on_delete=models.CASCADE, db_column='bairro_id', verbose_name='Bairro')
    valor_tae = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor_tae')
    data_registro = models.DateTimeField(auto_now_add=True, db_column='data_registro', verbose_name='Data de Registro')

    def __str__(self):
        return f"Estabelecimento {self.id}"
    class Meta:
        db_table = 'estabelecimento'