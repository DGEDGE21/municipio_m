from django.db import models
from django.contrib.auth.models import User
from Municipe.models import Municipe, Bairro
from Propriedade.models import Propriedade
from impostos.models import Imposto
from taxas.models import Taxa
from automovel.models import Automovel
from estabelecimento.models import Estabelecimento

class Pagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_pagamento')
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor')
    data = models.DateTimeField(auto_now_add=True, db_column='data')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, db_column='bairro_id', verbose_name='Bairro')
    metodo= models.CharField(max_length=100, null=True, db_column='metodo',default='Numerário')
    def __str__(self):
        return f"Pagamento {self.id}"

    class Meta:
        db_table = 'pagamento'

class IpaPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_ipa_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, related_name='ipa_pagamentos', db_column='id_municipe')
    imposto = models.ForeignKey(Imposto, on_delete=models.CASCADE, db_column='id_imposto')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')
    epoca = models.CharField(max_length=100, db_column='epoca')

    def __str__(self):
        return f"IpaPagamento {self.id}"

    class Meta:
        db_table = 'ipa_pagamento'

class PropPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_prop_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='id_propriedade')
    imposto = models.ForeignKey(Imposto, on_delete=models.CASCADE, db_column='id_imposto')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')
    epoca = models.CharField(max_length=100, db_column='epoca')

    def __str__(self):
        return f"PropPagamento {self.id}"

    class Meta:
        db_table = 'prop_pagamento'

class IavPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_iav_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    automovel = models.ForeignKey(Automovel, on_delete=models.CASCADE, db_column='id_automovel')
    imposto = models.ForeignKey(Imposto, on_delete=models.CASCADE, db_column='id_imposto')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')
    epoca = models.CharField(max_length=100, db_column='epoca')

    def __str__(self):
        return f"IavPagamento {self.id}"

    class Meta:
        db_table = 'iav_pagamento'

class TaePagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_tae_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE, db_column='id_estabelecimento')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')
    epoca = models.CharField(max_length=100, db_column='epoca')

    def __str__(self):
        return f"TaePagamento {self.id}"

    class Meta:
        db_table = 'tae_pagamento'

class DeclaracaoPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_declaracao_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')

    def __str__(self):
        return f"DeclaracaoPagamento {self.id}"

    class Meta:
        db_table = 'declaracao_pagamento'

class UrbPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_urb_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    propriedade = models.ForeignKey(Propriedade, on_delete=models.CASCADE, db_column='id_propriedade')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')

    def __str__(self):
        return f"UrbPagamento {self.id}"

    class Meta:
        db_table = 'urbanizacao_pagamento'

class PubPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_pub_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    unidade= models.CharField(max_length=100, db_column='unidade')
    tipo= models.CharField(max_length=100, db_column='tipo')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')

    def __str__(self):
        return f"PubPagamento {self.id}"

    class Meta:
        db_table = 'publicidade_pagamento'

class TransPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_pub_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')

    def __str__(self):
        return f"TransPagamento {self.id}"

    class Meta:
        db_table = 'transporte_pagamento'

class ResidualPagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_residual_pagamento')
    municipe = models.ForeignKey(Municipe, on_delete=models.CASCADE, db_column='id_municipe')
    taxa = models.ForeignKey(Taxa, on_delete=models.CASCADE, db_column='id_taxa')
    pagamento = models.ForeignKey(Pagamento, on_delete=models.CASCADE, db_column='id_pagamento')

    def __str__(self):
        return f"ResidualPagamento {self.id}"

    class Meta:
        db_table = 'residual_pagamento'

