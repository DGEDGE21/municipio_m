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

class DeclaracaoBaseSerializer(serializers.ModelSerializer):
    pagamento=DeclaracaoPagamentoSerializer()
    class Meta:
        model = DeclaracaoBase
        fields = '__all__'


class DeclaracaoCoabitacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoCoabitacao
        fields = '__all__'


class DeclaracaoPobrezaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoPobreza
        fields = '__all__'


class DeclaracaoResidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoResidencia
        fields = '__all__'


class DeclaracaoMatricialSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoMatricial
        fields = '__all__'


class DeclaracaoViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoViagem
        fields = '__all__'


class DeclaracaoCredencialViagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoCredencialViagem
        fields = '__all__'


class DeclaracaoObitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclaracaoObito
        fields = '__all__'
