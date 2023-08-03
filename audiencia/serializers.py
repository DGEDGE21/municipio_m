from rest_framework import serializers
from Municipe.models import Bairro, Municipe
from Municipe.serializers import *
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

#serializer de Audiencia
class AudienciaSerializer(serializers.ModelSerializer):
    municipe=MunicipeSerializer()
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Audiencia
        fields = ['id', 'municipe', 'data','hora','local','descricao','data_registo','estado','user']