from django.db import models
from django.contrib.auth.models import User
from Municipe.models import Municipe
# Create your models here.

class Audiencia(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_audiencia')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    data = models.DateField(db_column='data')
    hora = models.TimeField(db_column='hora')
    local = models.CharField(max_length=100, db_column='local')
    descricao = models.CharField(max_length=100, db_column='descricao')
    estado = models.CharField(max_length=100, db_column='estado')
    user = models.OneToOneField(User,null=True,  on_delete=models.CASCADE, db_column="utilizador")
    data_registo = models.DateField(auto_now=True, db_column='data_registo')
    def __str__(self):
        return f"{self.municipe.nome}- {self.data} - {self.hora} - {self.local} - {self.descricao} - {self.estado}"

    class Meta:
        db_table = 'audiencia'
