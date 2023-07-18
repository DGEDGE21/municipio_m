from rest_framework import serializers
from .models import Imposto

class ImpostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imposto
        fields = ['id', 'nome', 'rubrica', 'valor', 'destino', 'lei', 'periodicidade', 'data_maxima']
