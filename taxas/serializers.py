from rest_framework import serializers
from .models import Taxa

class TaxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxa
        fields = ['id', 'nome', 'rubrica', 'valor', 'destino', 'lei', 'periodicidade', 'data_maxima']
