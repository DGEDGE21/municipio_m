from django.db import models

class Taxa(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_taxa')
    nome = models.CharField(max_length=250, db_column='nome_taxa')
    rubrica = models.CharField(max_length=100, db_column='rubrica_taxa')
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor_taxa')
    destino = models.CharField(max_length=100, db_column='destino_taxa')
    lei = models.CharField(max_length=100, db_column='lei_taxa')
    periodicidade = models.CharField(max_length=100, db_column='periodicidade_taxa')
    data_maxima = models.DateField(db_column='data_maxima_taxa')

    def __str__(self):
        return f'{self.rubrica}-{self.nome}-{self.destino}'

    class Meta:
        db_table = 'taxa'
