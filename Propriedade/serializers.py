from rest_framework import serializers
from .models import Propriedade
from Municipe.models import Municipe, Bairro
from Municipe.serializers import MunicipeSerializer, BairroSerializer
from django.utils.timezone import localtime
from datetime import datetime

class PropriedadeCreateSerializer(serializers.ModelSerializer):
    nr_contribuente = serializers.CharField(write_only=True)
    bairro_id = serializers.IntegerField(write_only=True)
    valor_patrimonial = serializers.FloatField(read_only=True)  # Adiciona um campo para o valor patrimonial

    class Meta:
        model = Propriedade
        fields = ['id', 'nr_contribuente', 'quarteirao', 'nr_casa', 'bairro_id', 'natureza', 'tipo', 'data_licenca', 'area_edificada', 'area_logradouro', 'valor_patrimonial', 'data_registro']

    def create(self, validated_data):
        nr_contribuente = validated_data.pop('nr_contribuente')
        bairro_id = validated_data.pop('bairro_id')

        # Obtém o objeto Bairro com base no bairro_id
        bairro = Bairro.objects.get(id=bairro_id)

        # Obtém o objeto Municipe com base no nr_contribuente
        municipe = Municipe.objects.get(nr_contribuente=nr_contribuente)

        # Cálculo do valor patrimonial
        data_licenca = validated_data['data_licenca']
        ano = data_licenca.year
        actual =  datetime.now().year
        idade = actual - ano
        print(idade)
        fa = 0  # factor de antiguidade
        fi = 0.9  # factor de localizacao
        tipo = validated_data['tipo']
        areaE = validated_data['area_edificada']
        areaL = validated_data['area_logradouro']

        if tipo == "Habitacao":
            if idade < 5:
                fa = 0
            elif 5 <= idade <= 10:
                fa = 1
            elif 11 <= idade <= 15:
                fa = 0.95
            elif 16 <= idade <= 20:
                fa = 0.9
            elif 21 <= idade <= 30:
                fa = 0.85
            elif 31 <= idade <= 40:
                fa = 0.75
            elif 41 <= idade <= 50:
                fa = 0.65
            elif idade > 50:
                fa = 0.55
        else:
            if idade < 5:
                fa = 1
            elif 5 <= idade <= 10:
                fa = 0.95
            elif 11 <= idade <= 15:
                fa = 0.90
            elif 16 <= idade <= 20:
                fa = 0.85
            elif 21 <= idade <= 30:
                fa = 0.80
            elif 31 <= idade <= 40:
                fa = 0.75
            elif 41 <= idade <= 50:
                fa = 0.70
            elif idade > 50:
                fa = 0.65

        vp = (float(areaE) * 3000 * fa + 0.05 * float(areaL) * 3000) * fi
        validated_data['valor_patrimonial'] = vp

        # Cria a instância de Propriedade com os dados validados
        propriedade = Propriedade.objects.create(id_municipe=municipe, bairro=bairro, **validated_data)

        return propriedade

class PropriedadeSerializer(serializers.ModelSerializer):
    nr_contribuente = serializers.CharField(write_only=True)
    bairro_id = serializers.IntegerField(write_only=True)
    bairro=BairroSerializer()
    id_municipe=MunicipeSerializer()
    class Meta:
        model = Propriedade
        fields = ['id', 'nr_contribuente', 'id_municipe','bairro','quarteirao', 'nr_casa', 'bairro_id', 'natureza', 'tipo', 'data_licenca', 'area_edificada', 'area_logradouro', 'valor_patrimonial', 'data_registro']


