from rest_framework import serializers
from .models import Estabelecimento
from Municipe.models import Municipe, Bairro
from Municipe.serializers import MunicipeSerializer, BairroSerializer
from django.utils.timezone import localtime
from datetime import datetime

class EstabelecimentoCreateSerializer(serializers.ModelSerializer):
    nr_contribuente = serializers.CharField(write_only=True)
    bairro_id = serializers.IntegerField(write_only=True)
    valor_tae = serializers.FloatField(read_only=True)  # Adiciona um campo para o valor patrimonial

    class Meta:
        model = Estabelecimento
        fields = ['id', 'nr_contribuente', 'nome','area', 'sector', 'bairro_id','valor_tae']

    def create(self, validated_data):
        print(validated_data)
        nr_contribuente = validated_data.pop('nr_contribuente')
        bairro_id = validated_data.pop('bairro_id')

        # Obtém o objeto Bairro com base no bairro_id
        bairro = Bairro.objects.get(id=bairro_id)

        # Obtém o objeto Municipe com base no nr_contribuente
        municipe = Municipe.objects.get(nr_contribuente=nr_contribuente)

        # Cálculo do valor Tae
        sector=validated_data['sector']
        area=validated_data['area']

        if(sector=="Sector Comercial Geral"):
            if(area=="0-20 m2"):#de 0-20 m2
                valor=7738
            elif(area=="0-50 m2"):# de 0-50 m2
                valor=18233
            elif(area=="+50 m2"):# +50 m2
                valor=29589
        elif(sector=="Sector de Supermercados e Industrias"):
            if(area=="0-20 m2"):#de 0-20 m2
                valor=40474
            elif(area=="0-50 m2"):# de 0-50 m2
                valor=40871
            elif(area=="+50 m2"):# +50 m2
                valor=40871
        elif(sector=="Sector de Prestação de Serviço Geral"):
            if(area=="0-20 m2"):#de 0-20 m2
                valor=7738
            elif(area=="0-50 m2"):# de 0-50 m2
                valor=18233
            elif(area=="+50 m2"):# +50 m2
                valor=29520
        elif(sector=="Sector de Prestação de Serviços Financeiros"):
            if(area=="Microcredito"):#Microcredito
                valor=21630
            elif(area=="Casa de cambio"):#Casa de cambio
                valor=43688
            elif(area=="ATM"):#ATM
                valor=21630
            elif(area=="De 0-50 m2"):# De 0-50 m2
                valor=81915
            elif(area=="De 0-100 m2"):# De 0-100 m2
                valor=82718
            elif(area=="+100 m2"):# +100 m2
                valor=82718
        elif(sector=="Sector de Hotelaria, Restaurante e aluguer de Quartos"):
            if(area=="Aluguer de Quartos até 5"):#Aluguer de quartos até 5
                valor=13359
            elif(area=="Aluguer de Quartos +5"):#Aluguer de quartos mais de 5
                valor=40474
            elif(area=="De 0-50 m2"):# De 0-50 m2
                valor=40077
            elif(area=="De 0-100 m2"):# De 0-100 m2
                valor=40473
            elif(area=="+ 100 m2"):# +100 m2
                valor=40870

        
        validated_data['valor_tae'] = valor

        # Cria a instância de Propriedade com os dados validados
        estabelecimento = Estabelecimento.objects.create(id_municipe=municipe, bairro=bairro, **validated_data)

        return estabelecimento

class EstabelecimentoSerializer(serializers.ModelSerializer):
    nr_contribuente = serializers.CharField(write_only=True)
    bairro_id = serializers.IntegerField(write_only=True)
    bairro=BairroSerializer()
    id_municipe=MunicipeSerializer()
    class Meta:
        model = Estabelecimento
        fields = ['id', 'nr_contribuente', 'nome','id_municipe','bairro','bairro_id','sector', 'area', 'valor_tae','data_registro']


