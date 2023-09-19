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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import render
from automovel.models import *
from automovel.serializers import *
from Propriedade.models import *
from Propriedade.serializers import *
from estabelecimento.models import *
from estabelecimento.serializers import *
from pagamentos.models import *
from pagamentos.serializers import *
from datetime import datetime
from rest_framework.views import APIView
from automovel.views import calcula_iav
from licenciamento.models import *
from planificacao.models import *
from planificacao.serializers import *
from licenciamento.serializers import *

class MunicipeCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MunicipeCreateSerializer

class BairroListView(ListAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class MercadoListView(ListAPIView):
    queryset = Mercado.objects.all()
    serializer_class = MercadoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class MunicipeListView(ListAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class MunicipeDetailView(RetrieveAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'nr_contribuente'
    lookup_url_kwarg = 'nr_contribuente'

class MunicipeUpdateView(UpdateAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeUpdateSerializer
    lookup_field = 'id'  # Campo utilizado para a busca do objeto

    def get_serializer_context(self):
        # Inclui o request na contexto do serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class MunicipePagamentosView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None, **kwargs):
        nr_contribuinte = self.kwargs['nr_contribuinte']
        municipe = Municipe.objects.get(nr_contribuente=nr_contribuinte)
        current_year = datetime.now().year
        lista = []

        # Imposto Pessoal Autarquico
        if municipe.tipo_municipe == "Singular":
            #quero que no for seja de 2022 até o ano atual
            
            for ano in range(municipe.data_registro.year, current_year+1):
                print(ano)
                ipa_pagamento = IpaPagamento.objects.filter(municipe=municipe, epoca=ano).first()
                valor = ipa_pagamento.pagamento.valor if ipa_pagamento else 143
                situacao = "Pago" if ipa_pagamento else "Não Pago"
                data_pagamento = ipa_pagamento.pagamento.data.strftime('%Y-%m-%d') if ipa_pagamento else None

                lista.append({
                    "nr_contribuente":nr_contribuinte,
                    "epoca": ano,
                    "valor": valor,
                    "situacao": situacao,
                    "rubrica": 112101,
                    "tipo": "Imposto Pessoal Autarquico",
                    "dataPagamento": data_pagamento
                })

        # Imposto Autarquico de Veiculos
        for automovel in municipe.automovel_set.all():
            for ano in range(automovel.data_registro.year, current_year+1):
                iav_pagamento = IavPagamento.objects.filter(municipe=municipe, automovel=automovel, epoca=ano).first()
                auto_s=AutomovelSerializer(automovel)
                valor=calcula_iav(auto_s)
                situacao = "Pago" if iav_pagamento else "Não Pago"
                data_pagamento = iav_pagamento.pagamento.data.strftime('%Y-%m-%d')[:10] if iav_pagamento else None

                lista.append({
                    "nr_contribuente":nr_contribuinte,
                    "epoca": ano,
                    "valor": valor,
                    "situacao": situacao,
                    "rubrica":112202,
                    "tipo": "Imposto Autarquico de Veiculos",
                    "matricula": automovel.matricula,
                    "dataPagamento": data_pagamento
                })

        # Imposto Autarquico de Propriedade
        for propriedade in municipe.propriedade_set.all():
            for ano in range(propriedade.data_registro.year, current_year+1):
                prop_pagamento = PropPagamento.objects.filter(municipe=municipe, propriedade=propriedade, epoca=ano).first()
                #o valor sera o valor patrimonial vezes 0.007 se a propriedade for tipo habitaca e 0.002 se for rural
                valor = float(propriedade.valor_patrimonial) * 0.007 if propriedade.tipo == "Habitacao" else float(propriedade.valor_patrimonial) * 0.004
                situacao = "Pago" if prop_pagamento else "Não Pago"
                data_pagamento = prop_pagamento.pagamento.data.strftime('%Y-%m-%d')[:10] if prop_pagamento else None
                #arrendoda o valor para 2 casas decimais
                valor = round(valor, 2)
                lista.append({
                    "nr_contribuente":nr_contribuinte,
                    "epoca": ano,
                    "valor": (valor),
                    "situacao": situacao,
                    "rubrica":112203,
                    "tipo": "Imposto Predial Autarquico",
                    "propriedade": propriedade.id,
                    "dataPagamento": data_pagamento
                })

        # Taxa de Actividade Económica
        for estabelecimento in municipe.estabelecimento_set.all():
            for ano in range(estabelecimento.data_registro.year, current_year+1):
                tae_pagamento = TaePagamento.objects.filter(municipe=municipe, estabelecimento=estabelecimento, epoca=ano).first()
                valor_total = tae_pagamento.pagamento.valor if tae_pagamento else 0
                saldo = float(estabelecimento.valor_tae) - float(valor_total)
                situacao = "Pago" if saldo <= 0 else "Não Pago"
                data_pagamento = tae_pagamento.pagamento.data.strftime('%Y-%m-%d')[:10] if tae_pagamento and situacao == "Pago" else None

                lista.append({
                    "nr_contribuente":nr_contribuinte,
                    "epoca": ano,
                    "valor": estabelecimento.valor_tae,
                    "situacao": situacao,
                    "rubrica":114108,
                    "tipo": "Taxa de Actividade Económica",
                    "estabelecimento": estabelecimento.id,
                    "dataPagamento": data_pagamento
                })

        return Response(lista, status=200)

class cadastrar_mercados(APIView):
    def post(self, request, format=None):
        mercados = request.data.get('mercados')
        for mercado in mercados:
            nome=mercado.get('mercado')
            mercado_obj = Mercado.objects.create(
                nome=nome,
            )
            mercado_obj.save()
        return Response(data={"success": True})

class LicensasListView(ListAPIView):

    def get(self, request, format=None, **kwargs):
        municipe = Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuente'])
        todas_declaracoes = (
                list(LicensaAE.objects.filter(pagamento__municipe=municipe)) +
                list(LicensaAgua.objects.filter(pagamento__municipe=municipe)) +
                list(LicensaTransporte.objects.filter(pagamento__municipe=municipe))
            )

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, LicensaAgua):
                serializer = LicensaAguaSerializer(declaracao)
            elif isinstance(declaracao, LicensaTransporte):
                serializer = LicensaTransporteSerializer(declaracao)
            elif isinstance(declaracao, LicensaAE):
                serializer = LicensaAESerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue
            serialized_declaracoes.append(serializer.data)

        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)
