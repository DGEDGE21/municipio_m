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
from rest_framework.views import APIView

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
                    saldo=prop.valor_tae-valor_total
                    situacao.append(
                        {"Ano": epoca_str, "situacao": "Pago" if valor_total>=prop.valor_tae else "Não Pago", "saldo":saldo,"valor_total": valor_total})
                else:
                    situacao.append(
                        {"Ano": epoca_str, "situacao": "Não Pago", "valor_total": 0, "saldo":prop.valor_tae	})

            # Adiciona o resultado para o munícipe atual
            prop_s = EstabelecimentoSerializer(prop).data
            prop_s['situacao'] = situacao
            result.append(prop_s)

        print(result)
        return Response(result)

def calcular_taxa_urbanizacao_cat1(self, rubrica):
    taxas = {
        "urb11": {"nacional": 15.00, "estrangeiro": 20.00, "taxa_fixa": 900.00},
        "urb12": {"nacional": 7.50, "estrangeiro": 15.00},
        "urb13": {"nacional": 20.00, "estrangeiro": 25.00},
        "urb14": {"nacional": 10.00, "estrangeiro": 25.00},
        "urb21": {"nacional": 1.50, "estrangeiro": 3.00},
        "urb22": {"nacional": 10.00, "estrangeiro": 15.00},
        "urb23": {"nacional": 12.00, "estrangeiro": 20.00},
        "urb24": {"nacional": 10.00, "estrangeiro": 20.00},
        "urb25": {"nacional": 4.00, "estrangeiro": 6.00},
        "urb26": {"nacional": 20.00, "estrangeiro": 30.00}
    }

    taxa_info = taxas.get(rubrica)
    if not taxa_info:
        raise ValueError("Taxa não encontrada.")

    valor_metro_quadrado = taxa_info["nacional"]
    if self.id_municipe.nacionalidade != "Moçambicano(a)":
        valor_metro_quadrado = taxa_info["estrangeiro"]

    valor_taxa = float(self.area_logradouro) * valor_metro_quadrado
    if "taxa_fixa" in taxa_info:
        valor_taxa += taxa_info["taxa_fixa"]

    return valor_taxa

def calcular_taxa_urbanizacao_cat2(self, rubrica, area):
        taxas = {
            "urb51": {"bairros": [5,6], "taxa_fixa": 900.00},
            #"urb51": {"nacional": 5.00, "bairros": [7,8,9, 10, 11, 12, 13, 14, 15, 16, 17, 18]},
            "urb61": {"pequena_edificacao": 1500.00, "grande_edificacao": 3000.00},
            "urb81": {"pequena_edificacao": 1500.00, "grande_edificacao": 3000.00}
        }

        # Cálculo para a taxa de apreciação de projetos de construções novas
        if rubrica == "urb51":
            if int(self.bairro.id) in taxas["urb51"]["bairros"]:
                valor_taxa = area * 6.00 + taxas["urb51"]["taxa_fixa"]
            else :
                valor_taxa = area * 5.00 + taxas["urb51"]["taxa_fixa"]
        elif rubrica == "urb61":
            if area <= 199:
                valor_taxa = taxas["urb61"]["pequena_edificacao"]
            else:
                valor_taxa = taxas["urb61"]["grande_edificacao"]
        elif rubrica == "urb81":
            if area <= 199:
                valor_taxa = taxas["urb81"]["pequena_edificacao"] * (1/3)
            else:
                valor_taxa = taxas["urb81"]["grande_edificacao"]  * (2/3)
        else:
            raise ValueError("Taxa não encontrada.")
        #aproxima o valor para cima para não haver decimais
        valor_taxa=round(valor_taxa)
        return valor_taxa

def calcular_taxa_urbanizacao_cat3(self, rubrica):
        taxas = {
            "urb71": {"valor":2400},
            "urb81": {"valor":1200},
            "urb10": {"valor":1000},
            "urb111": {"valor":1500},
        }

        # Cálculo para a taxa de apreciação de projetos de construções novas
        if rubrica == "urb71":
            valor_taxa = taxas["urb71"]["valor"]
        elif rubrica == "urb81":
            valor_taxa = taxas["urb81"]["valor"]
        elif rubrica == "urb10":
            valor_taxa = taxas["urb10"]["valor"]
        elif rubrica == "urb111":
            valor_taxa = taxas["urb111"]["valor"]
        else:
            raise ValueError("Taxa não encontrada.")
    
        return valor_taxa

def calcular_taxa_publicidade(rubrica, tipo, unit):
        taxas = {
            "pub1": {"letra":35,"imagem":200},
            "pub2": {"valor":2000},
            "pub3": {"valor":2500},
            "pub4": {"valor":2000},
        }

        # Cálculo para a taxa de apreciação de projetos de construções novas
        if rubrica == "pub1" and tipo=="letra":
            valor_taxa = taxas["pub1"]["letra"] * int(unit)
        elif rubrica == "pub1" and tipo=="imagem":
            valor_taxa = taxas["pub1"]["imagem"] * int(unit)
        elif rubrica == "pub2":
            valor_taxa = taxas["pub2"]["valor"] * int(unit)
        elif rubrica == "pub3":
            valor_taxa = taxas["pub3"]["valor"] * int(unit)
        elif rubrica == "pub4":
            valor_taxa = taxas["pub4"]["valor"] * int(unit)
        else:
            raise ValueError("Taxa não encontrada.")
    
        return valor_taxa

class calculo_urbanizacao(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        id=self.request.data['id']
        rubrica=self.request.data['rubrica']
        area=self.request.data['area']
        prop=Propriedade.objects.get(id=id)
        taxa=Taxa.objects.get(rubrica=rubrica)
        rubrica=taxa.rubrica
        if(taxa.destino=="urbanizacao-cat1" or taxa.destino=='urbanizacao-cat2'):
            valor=calcular_taxa_urbanizacao_cat1(prop, rubrica)
        elif(taxa.destino=="urbanizacao-cat5" or taxa.destino=="urbanizacao-cat6" or taxa.destino=="urbanizacao-cat8"):
            valor=calcular_taxa_urbanizacao_cat2(prop, rubrica, float(area))
        elif(taxa.destino=="urbanizacao-cat7"  
             or taxa.destino=="urbanizacao-cat10" or taxa.destino=="urbanizacao-cat11"):
            valor=calcular_taxa_urbanizacao_cat3(prop, rubrica)
        print(valor)
        return Response(data={"valor": valor})

class calculo_publicidade(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        rubrica=self.request.data['rubrica']
        tipo=self.request.data['tipo']
        unit=self.request.data['unit']
        valor=calcular_taxa_publicidade(rubrica, tipo, unit)
        

        return Response(data={"valor": valor})