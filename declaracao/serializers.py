from rest_framework import serializers
from .models import (
    DeclaracaoBase,
    DeclaracaoCoabitacao,
    DeclaracaoPobreza,
    DeclaracaoResidencia,
    DeclaracaoMatricial,
    DeclaracaoViagem,
    DeclaracaoCredencialViagem,
    DeclaracaoObito,
)
from pagamentos.serializers import *

class DeclaracaoSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoBase
        fields = '__all__'


class DeclaracaoCoabitacaoSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoCoabitacao
        fields = '__all__'


class DeclaracaoPobrezaSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoPobreza
        fields = '__all__'


class DeclaracaoResidenciaSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoResidencia
        fields = '__all__'


class DeclaracaoMatricialSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoMatricial
        fields = '__all__'


class DeclaracaoViagemSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoViagem
        fields = '__all__'


class DeclaracaoCredencialViagemSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoCredencialViagem
        fields = '__all__'


class DeclaracaoObitoSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoObito
        fields = '__all__'
