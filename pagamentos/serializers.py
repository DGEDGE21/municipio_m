from rest_framework import serializers
from .models import *
from Municipe.serializers import *
from impostos.serializers import *
from Propriedade.serializers import *
from automovel.serializers import *
from taxas.serializers import *
from estabelecimento.serializers import *
from rest_framework import serializers

class PagamentoSerializer(serializers.ModelSerializer):
    bairro=BairroSerializer()
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Pagamento
        fields = ['id', 'valor', 'bairro','data','metodo','user']

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

class UrbPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    propriedade=PropriedadeSerializer
    class Meta:
        model = PropPagamento
        fields = ['id', 'municipe', 'propriedade','taxa', 'pagamento']

class PubPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    class Meta:
        model = PubPagamento
        fields = ['id', 'municipe', 'taxa', 'unidade','tipo','pagamento']

class TransPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    class Meta:
        model = TransPagamento
        fields = ['id', 'municipe', 'taxa','pagamento']

class ResidualPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    class Meta:
        model = ResidualPagamento
        fields = ['id', 'municipe', 'taxa','pagamento']

class MercadoPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    mercado=MercadoSerializer()
    class Meta:
        model = MercadoPagamento
        fields = ['id', 'municipe', 'mercado', 'taxa','pagamento']

class GenericoPagamentoSerializer(serializers.ModelSerializer):
    municipe = MunicipeSerializer()
    taxa = TaxaSerializer()
    pagamento = PagamentoSerializer()
    class Meta:
        model = GenericoPagamento
        fields = ['id', 'municipe', 'taxa','pagamento']



