from rest_framework import serializers
from .models import *
from Municipe.models import *
from Municipe.serializers import *

class AutomovelSerializer(serializers.ModelSerializer):
    nr_contribuente = serializers.CharField(write_only=True)
    id_municipe=MunicipeSerializer()
    class Meta:
        model = Automovel
        fields = ['id', 'id_municipe','nr_contribuente','matricula', 'marca', 'modelo', 'combustivel', 'cilindrada', 'lotacao', 'ano_fabrico', 'ano_compra', 'tipo', 'natureza', 'capacidade_carga']

    def create(self, validated_data):
        nr_contribuente = validated_data.pop('nr_contribuente')
        municipe = Municipe.objects.get(nr_contribuente=nr_contribuente)
        automovel = Automovel.objects.create(id_municipe=municipe, **validated_data)
        return automovel

class Automovel_Grupo_Escalao_Serializado(serializers.ModelSerializer):
    class Meta:
        model=Automovel_Grupo_Escalao
        fields='__all__'

class Automovel_Grupo_Serializado(serializers.ModelSerializer):
    class Meta:
        model=Automovel_Grupo
        fields='__all__'