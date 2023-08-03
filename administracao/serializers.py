from rest_framework import serializers
from Municipe.models import Bairro, Municipe
from Municipe.serializers import *
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *

class UnidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    municipe=MunicipeSerializer()
    unidade=UnidadeSerializer()
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Funcionario
        fields = ['id', 'municipe', 'unidade','cargo','user', 'isActive']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name','last_name')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'])
        user.set_password('girp2023')
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.save()

        return user


