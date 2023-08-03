from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from .models import *
from .serializers import *
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.shortcuts import render
from pagamentos.models import *
from Municipe.models import *
from Municipe.serializers import *
from Propriedade.serializers import *
from automovel.views import calcula_iav 
from automovel.serializers import *
from datetime import datetime

class ImpostoListView(ListAPIView):
    queryset = Imposto.objects.all()
    serializer_class = ImpostoSerializer

class ImpostoDetailView(RetrieveAPIView):
    queryset = Imposto.objects.all()
    serializer_class = ImpostoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'rubrica'
    lookup_url_kwarg = 'rubrica'

class MunicipeListAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Obtém todos os munícipes
        queryset = Municipe.objects.all()

        # Calcula o número de épocas a partir de 2022 até o ano atual
        current_year = datetime.now().year
        start_year = 2022
        num_epocas = current_year - start_year + 1

        # Lista para armazenar o resultado
        result = list()

        # Verifica a existência do objeto IpaPagamento para cada munícipe e época
        for municipe in queryset:
            situacao = list()

            for epoca in range(start_year, current_year + 1):
                epoca_str = str(epoca)
                ipa_pagamento_exists = IpaPagamento.objects.filter(municipe=municipe, epoca=epoca_str).exists()
                situacao.append({"Ano":epoca_str,'situacao':"Pago"}) if ipa_pagamento_exists else situacao.append({"Ano":epoca_str,'situacao':"Não Pago"})
        
            # Adiciona o resultado para o munícipe atual
            mun_s=MunicipeSerializer(municipe).data
            mun_s['situacao']=situacao
            mun_s['valor']=Imposto.objects.get(rubrica='112101').valor
            print(mun_s)
            result.append(
                mun_s
            )

        return Response(result)

class PropriedadeListAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Obtém todos os munícipes
        queryset = Propriedade.objects.all()

        # Calcula o número de épocas a partir de 2022 até o ano atual
        current_year = datetime.now().year
        start_year = 2022
        num_epocas = current_year - start_year + 1

        # Lista para armazenar o resultado
        result = list()

        # Verifica a existência do objeto IpaPagamento para cada munícipe e época
        for prop in queryset:
            situacao = list()

            for epoca in range(start_year, current_year + 1):
                epoca_str = str(epoca)
                prop_pagamento_exists = PropPagamento.objects.filter(propriedade=prop, epoca=epoca_str, imposto__rubrica="112203").exists()
                situacao.append({"Ano":epoca_str,'situacao':"Pago"}) if prop_pagamento_exists else situacao.append({"Ano":epoca_str,'situacao':"Não Pago"})
        
            # Adiciona o resultado para o munícipe atual
            prop_s=PropriedadeSerializer(prop).data
            if(prop_s['tipo']=='Habitacao'):
                valor= float(prop_s['valor_patrimonial'])*0.004
            else:
                valor= float(prop_s['valor_patrimonial'])*0.007
            prop_s['situacao']=situacao
            prop_s['valor_ipra']=valor
            print(prop_s)
            result.append(
                prop_s
            )

        return Response(result)
    
class AutomovelListAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Obtém todos os munícipes
        queryset = Automovel.objects.all()

        # Calcula o número de épocas a partir de 2022 até o ano atual
        current_year = datetime.now().year
        start_year = 2022
        num_epocas = current_year - start_year + 1

        # Lista para armazenar o resultado
        result = list()

        # Verifica a existência do objeto IpaPagamento para cada munícipe e época
        for auto in queryset:
            situacao = list()
            valorIAV=calcula_iav(AutomovelSerializer(auto))
            for epoca in range(start_year, current_year + 1):
                epoca_str = str(epoca)
                iav_pagamento_exists = IavPagamento.objects.filter(automovel=auto, epoca=epoca_str, imposto__rubrica="112202").exists()
                situacao.append({"Ano":epoca_str,'situacao':"Pago"}) if iav_pagamento_exists else situacao.append({"Ano":epoca_str,'situacao':"Não Pago"})
        
            # Adiciona o resultado para o munícipe atual
            auto_s=AutomovelSerializer(auto).data
            auto_s['situacao']=situacao
            auto_s['valor']=valorIAV
            print(auto_s)
            result.append(
                auto_s
            )

        return Response(result)