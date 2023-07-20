from rest_framework import serializers
from .models import *
from Municipe.serializers import *
from impostos.serializers import *
from Propriedade.serializers import *
from automovel.serializers import *
from taxas.serializers import *
from estabelecimento.serializers import *

class PagamentoSerializer(serializers.ModelSerializer):
    bairro=BairroSerializer()
    class Meta:
        model = Pagamento
        fields = ['id', 'valor', 'bairro','data']

class IpaPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    imposto = ImpostoSerializer()
    pagamento = PagamentoSerializer()

    class Meta:
        model = IpaPagamento
        fields = ['id', 'municipe', 'imposto', 'pagamento', 'epoca']

class PropPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    imposto = ImpostoSerializer()
    pagamento = PagamentoSerializer()
    propriedade=PropriedadeSerializer
    class Meta:
        model = PropPagamento
        fields = ['id', 'municipe', 'propriedade','imposto', 'pagamento', 'epoca']

class IavPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    imposto = ImpostoSerializer()
    pagamento = PagamentoSerializer()
    automovel=AutomovelSerializer()
    class Meta:
        model = IavPagamento
        fields = ['id', 'municipe', 'automovel','imposto', 'pagamento', 'epoca']

class TaePagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    estabelecimento=EstabelecimentoSerializer()
    class Meta:
        model = TaePagamento
        fields = ['id', 'municipe', 'estabelecimento','taxa', 'pagamento', 'epoca']

class DeclaracaoPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    class Meta:
        model = TaePagamento
        fields = ['id', 'municipe', 'taxa', 'pagamento']