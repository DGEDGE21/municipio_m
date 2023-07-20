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
from estabelecimento.serializers import *


class TaxaListView(ListAPIView):
    queryset = Taxa.objects.all()
    serializer_class = TaxaSerializer


class TaxaDetailView(RetrieveAPIView):
    queryset = Taxa.objects.all()
    serializer_class = TaxaSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'rubrica'
    lookup_url_kwarg = 'rubrica'


class EstabelecimentoListAPIView(CreateAPIView):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Obtém todos os munícipes
        queryset = Estabelecimento.objects.all()

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
                valor_total = 0
                epoca_str = str(epoca)
                estab_pagamento_exists = TaePagamento.objects.filter(
                    estabelecimento=prop, epoca=epoca_str, taxa__rubrica="114108").exists()

                if estab_pagamento_exists:
                    tae_pagamentos = TaePagamento.objects.filter(
                        estabelecimento=prop, epoca=epoca_str, taxa__rubrica="114108")
                    valor_total = 0

                    for tae_pagamento in tae_pagamentos:
                        valor_total += tae_pagamento.pagamento.valor
                
                    situacao.append(
                        {"Ano": epoca_str, "situacao": "Pago" if valor_total>=prop.valor_tae else "Não Pago", "valor_total": valor_total})
                else:
                    situacao.append(
                        {"Ano": epoca_str, "situacao": "Não Pago", "valor_total": 0})

            # Adiciona o resultado para o munícipe atual
            prop_s = EstabelecimentoSerializer(prop).data
            prop_s['situacao'] = situacao
            result.append(prop_s)

        return Response(result)
