from django.db import models
from django.contrib.auth.models import User
from Municipe.models import Municipe, Bairro
from Propriedade.models import Propriedade
from impostos.models import Imposto
from automovel.models import Automovel
class Pagamento(models.Model):
    id = models.AutoField(primary_key=True, db_column='id_pagamento')
    valor = models.DecimalField(max_digits=10, decimal_places=2, db_column='valor')
    data = models.DateTimeField(auto_now_add=True, db_column='data')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE, db_column='bairro_id', verbose_name='Bairro')

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
