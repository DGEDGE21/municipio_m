from django.db import models
from django.contrib.auth.models import User

class Bairro(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_bairro')
    nome = models.CharField(max_length=100, db_column='nome_bairro', verbose_name='Nome do Bairro')

    class Meta:
        db_table = 'bairro'

    def __str__(self):
        return f'{self.id}-{self.nome}'

class Mercado(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_mercado')
    nome = models.CharField(max_length=100, db_column='nome_mercado', verbose_name='Nome do Mercado')

    class Meta:
        db_table = 'mercado'

    def __str__(self):
        return f'{self.id}-Mercado {self.nome}'

class Municipe(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_municipe')
    nome = models.CharField(max_length=100, db_column='nome_municipe', verbose_name='Nome')
    data_nascimento = models.DateField(db_column='data_nascimento', verbose_name='Data de Nascimento')
    genero = models.CharField(max_length=20, db_column='genero')
    nacionalidade = models.CharField(max_length=50, db_column='nacionalidade', default='Moçambicano(a)')
    nuit = models.CharField(max_length=20, db_column='nuit')
    bilhete_identidade = models.CharField(max_length=20, db_column='bilhete_identidade', verbose_name='Bilhete de Identidade')
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, db_column='bairro_id', verbose_name='Bairro')
    telefone = models.CharField(max_length=20, db_column='telefone')
    email = models.CharField(max_length=100, db_column='email', null=True)
    tipo_municipe = models.CharField(max_length=100, db_column='tipo_municipe', verbose_name='Tipo de Municipe')
    nr_contribuente = models.CharField(max_length=20, null=True, db_column='nr_contribuente', verbose_name='Número de Contribuinte')
    data_registro = models.DateTimeField(auto_now_add=True, db_column='data_registro', verbose_name='Data de Registro')
    user = models.OneToOneField(User,null=True,  on_delete=models.CASCADE, db_column="utilizador")
    
    class Meta:
        db_table = 'municipe'

    def __str__(self):
        return self.nome

