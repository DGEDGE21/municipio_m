from django.db import models

class Imposto(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_imposto')
    nome = models.CharField(max_length=100, db_column='nome_imposto')
    rubrica = models.CharField(max_length=100, db_column='rubrica_imposto')
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor_imposto')
    destino = models.CharField(max_length=100, db_column='destino_imposto')
    lei = models.CharField(max_length=100, db_column='lei_imposto')
    periodicidade = models.CharField(max_length=100, db_column='periodicidade_imposto')
    data_maxima = models.DateField(db_column='data_maxima_imposto')

    def __str__(self):
        return f'{self.rubrica}-{self.nome}'

    class Meta:
        db_table = 'imposto'
