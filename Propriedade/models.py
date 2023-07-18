from django.db import models
from Municipe.models import Municipe, Bairro

class Propriedade(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_propriedade')
    id_municipe = models.ForeignKey(Municipe,on_delete=models.CASCADE, db_column='id_Municipe')
    quarteirao = models.CharField(max_length=100, db_column='quarteirao')
    nr_casa = models.CharField(max_length=20, db_column='nr_casa')
    bairro = models.ForeignKey(Bairro, null=True,on_delete=models.CASCADE, db_column='bairro_id', verbose_name='Bairro')
    natureza = models.CharField(max_length=100, db_column='natureza')
    tipo = models.CharField(max_length=100, db_column='tipo')
    data_licenca = models.DateField(db_column='data_licenca')
    area_edificada = models.DecimalField(max_digits=10, decimal_places=2, db_column='area_edificada')
    area_logradouro = models.DecimalField(max_digits=10, decimal_places=2, db_column='area_logradouro')
    valor_patrimonial = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor_patrimonial')
    data_registro = models.DateTimeField(auto_now_add=True, db_column='data_registro', verbose_name='Data de Registro')

    def __str__(self):
        return f"Propriedade {self.id}"
    class Meta:
        db_table = 'propriedade'