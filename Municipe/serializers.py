from rest_framework import serializers
from .models import Bairro, Municipe, Mercado
from django.contrib.auth.models import User, Group


class BairroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bairro
        fields = '__all__'

class MercadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mercado
        fields = '__all__'

class MunicipeCreateSerializer(serializers.ModelSerializer):
    bairro_id = serializers.PrimaryKeyRelatedField(queryset=Bairro.objects.all(), source='bairro', write_only=True)
    class Meta:
        model = Municipe
        fields = ['id','nome', 'data_nascimento', 'nacionalidade','genero', 'nuit', 'bilhete_identidade', 'bairro_id', 'telefone', 'email', 'tipo_municipe', 'nr_contribuente', 'data_registro']
    
    def create(self, validated_data):
        bairro_id = validated_data.pop('bairro').id

        # Gera o número de contribuinte
        contribuinte_number = self.generate_contribuinte_number(bairro_id)
        validated_data['nr_contribuente'] = contribuinte_number

        # Criar usuário
        #cria o username com o nome e outrous criterios para garantir que seja unico
        username = validated_data['telefone']
        user = User.objects.create(username=username)
        user.set_password(contribuinte_number)
        user.save()

        # Adicionar usuário ao grupo "municipe"
        group = Group.objects.get(name='municipe')
        user.groups.add(group)

        municipe = Municipe.objects.create(bairro_id=bairro_id, user=user, **validated_data)
        return municipe

    def generate_contribuinte_number(self, bairro_id):
        bairro = Bairro.objects.get(id=bairro_id)
        user_count = User.objects.filter(groups__name='municipe').count()
        contribuinte_number = f"0010{bairro_id}{user_count + 1:03d}"
        return contribuinte_number

class MunicipeSerializer(serializers.ModelSerializer):
    bairro_id = serializers.PrimaryKeyRelatedField(queryset=Bairro.objects.all(), source='bairro', write_only=True)
    bairro=BairroSerializer()
    class Meta:
        model = Municipe
        fields = ['id','nome', 'data_nascimento', 'genero', 'nacionalidade', 'nuit', 'bilhete_identidade', 'bairro_id', 'bairro', 'telefone', 'email', 'tipo_municipe', 'nr_contribuente', 'data_registro']
    

class MunicipeUpdateSerializer(serializers.ModelSerializer):
    bairro_id = serializers.PrimaryKeyRelatedField(queryset=Bairro.objects.all(), source='bairro', required=False)

    class Meta:
        model = Municipe
        fields = ['id', 'nome', 'data_nascimento', 'nacionalidade', 'genero', 'nuit', 'bilhete_identidade', 'bairro_id', 'telefone', 'email', 'tipo_municipe', 'nr_contribuente', 'data_registro']

    def update(self, instance, validated_data):
        bairro_id = validated_data.pop('bairro_id', None)
        if bairro_id is not None:
            instance.bairro_id = bairro_id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name','last_name')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data['email'])
        user.set_password('girp2023')
        user.first_name=validated_data['first_name']
        user.last_name=validated_data['last_name']
        user.save()

        return user