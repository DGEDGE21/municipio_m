from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from .models import *
from .serializers import *
from django.utils import timezone
import pytz
from time import *
from datetime import *
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.shortcuts import render
from rest_framework.views import APIView
from pagamentos.models import UrbPagamento

class LicensaCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        id=request.data['id']
        dados=request.data['dados']
        user = request.user
        usuario = User.objects.get(username=user)

        urb=UrbPagamento.objects.get(pagamento__id=id)
        destino=urb.taxa.destino  
        print(urb.taxa.destino)
        if destino=='urbanizacao-cat1':
            dcl=LicensaDuat.objects.create(
                nome=dados['nome'],
                data_nasc=dados['data_nasc'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                bairro=dados['bairro'],
                area=dados['area'],
                quarteirao=dados['quarteirao'],
                data_atribuicao=dados['data_atribuicao'],
                pagamento=urb,
                user=usuario
            )
        elif destino=='urbanizacao-cat6':
            dcl=LicensaConstrucao.objects.create(
                nome=dados['nome'],
                data_nasc=dados['data_nasc'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                bairro=dados['bairro'],
                area_lougradouro=dados['area_lougradouro'],
                area_construcao=dados['area_construcao'],
                nr_pisos=dados['nr_pisos'],
                destino_obra=dados['destino_obra'],
                valor_obra=dados['valor_obra'],
                regime_obra=dados['regime_obra'],
                responsavel_obra=dados['responsavel_obra'],
                responsavel_nr=dados['responsavel_nr'],
                pagamento=urb,
                user=usuario
            )  
        
        if isinstance(dcl, LicensaDuat):
            serializer = LicensaDuatSerializer(dcl)
        elif isinstance(dcl, LicensaConstrucao):
            serializer = LicensaConstrucaoSerializer(dcl)
        print(serializer.data)
        return Response(serializer.data)

class LicensaAprovarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        destino = self.request.data['destino']
        id = self.request.data['id']
        if destino == "urbanizacao-cat1":
            licensa = LicensaDuat.objects.get(id=id)
        elif destino == "urbanizacao-cat6":
            licensa = LicensaConstrucao.objects.get(id=id)
        else:
            return Response(status=400)

        licensa.status = "Aprovado"
        #AttributeError: type object 'datetime.timezone' has no attribute 'now'
        licensa.data_aprovacao = datetime.now()
        licensa.save()
        return Response(status=200)

#Listar todas as Licensas de LicensaDuat, LicensaConstrucao que tenham status Aguardando Aprovacao
class LicensaListView(ListAPIView):    
    serializer_class = LicensaSerializer
    def get(self, request, format=None):
        todas_declaracoes = (
                list(LicensaConstrucao.objects.all()) +
                list(LicensaDuat.objects.all()) 
            )
        #filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if declaracao.status == "Aguardando Aprovacao"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, LicensaDuat):
                serializer = LicensaDuatSerializer(declaracao)
            elif isinstance(declaracao, LicensaConstrucao):
                serializer = LicensaConstrucaoSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)
        
        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)

class LicensaAprovedView(ListAPIView):    
    serializer_class = LicensaSerializer
    def get(self, request, format=None):
        todas_declaracoes = (
                list(LicensaConstrucao.objects.all()) +
                list(LicensaDuat.objects.all()) 
            )
        #filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if declaracao.status == "Aprovado"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, LicensaDuat):
                serializer = LicensaDuatSerializer(declaracao)
            elif isinstance(declaracao, LicensaConstrucao):
                serializer = LicensaConstrucaoSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)
        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)
