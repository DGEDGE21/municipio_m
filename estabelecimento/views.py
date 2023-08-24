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
from django.db.models import Q

class EstabelecimentoCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(self.request.data)

        dados=self.request.data
        # Obtém o objeto Bairro com base no bairro_id
        bairro = Bairro.objects.get(id=dados['bairro_id'])

        # Obtém o objeto Municipe com base no nr_contribuente
        municipe = Municipe.objects.get(nr_contribuente=dados['nr_contribuente'])

        # Cálculo do valor Tae
        sector=dados['sector']
        area=dados['area']

        print(sector)
        print(area)

        if sector == 'Categoria de Comércio Geral':
            if area == '0-20 m2':
                valor = 16110.90
            elif area == '21-30 m2':
                valor = 18720
            elif area == '+31 m2':
                valor = 19468.80
            elif area == 'Comércio a Grosso de 0 a 20m2':
                valor = 23400  # Coloca o valor apropriado aqui
            elif area == 'Armazéns desanexados dos estabelecimentos de 0 a 20m2':
                valor = 18720  # Coloca o valor apropriado aqui
            elif area == 'Distribuidores de 0 a 50m2':
                valor = 37908  # Coloca o valor apropriado aqui
            elif area == 'Distribuidores +50m2':
                valor = 46800  # Coloca o valor apropriado aqui

        elif sector == 'Categoria de Prestações de Serviço em Geral':
            if area == 'Ornamentação de Eventos e produção de bolos 0-50 m2':
                valor = 16110.90  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento de 0-50 m2':
                valor = 18720  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento de 51-100 m2':
                valor = 20280  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento +100 m2':
                valor = 23400  # Coloca o valor apropriado aqui

        elif sector == 'Categoria de Prestações de Serviços Financeiros':
            if area == 'Serviços Bancários de Micro-créditos':
                valor = 20280  # Coloca o valor apropriado aqui
            elif area == 'Serviços Bancários de Câmbios':
                valor = 23400  # Coloca o valor apropriado aqui
            elif area == 'Serviços Bancários de ATM':
                valor = 25000  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento Bancário de 0-50 m2':
                valor = 50544  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento Bancário de 51-100 m2':
                valor = 54756  # Coloca o valor apropriado aqui
            elif area == 'Estabelecimento Bancário com +100 m2':
                valor = 63180  # Coloca o valor apropriado aqui

        elif sector == 'Categoria de Hotelaria e Aluguer de Quartos':
            if area == 'Aluguer até 9 Quartos':
                valor = 19468.80  # Coloca o valor apropriado aqui
            elif area == 'Aluguer +10 Quartos':
                valor = 23400  # Coloca o valor apropriado aqui
            elif area == "Aluguer por cada Chalt's":
                valor = 12216.80  # Coloca o valor apropriado aqui
            elif area == 'Hotelaria de 0-50 m2':
                valor = 28415.40  # Coloca o valor apropriado aqui
            elif area == 'Hotelaria de 51-100 m2':
                valor = 30783.35  # Coloca o valor apropriado aqui
            elif area == 'Hotelaria com +100 m2':
                valor = 37908  # Coloca o valor apropriado aqui
        elif sector == 'Categoria de Restauração':
            if area == 'Centros Sociais e Take-Way':
                valor = 19468.80  # Coloque o valor apropriado aqui
            elif area == 'Restaurantes':
                valor = 28080  # Coloque o valor apropriado aqui
            elif area == 'Restauração com hospedagem':
                valor = 37908  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Aluguer de Imóveis Para Comércio e Habitação':
            if area == 'Aluguer de Casa de tipo 1':
                valor = 1200  # Coloque o valor apropriado aqui
            elif area == 'Aluguer de Casa de tipo 2':
                valor = 2200  # Coloque o valor apropriado aqui
            elif area == 'Aluguer de Casa de tipo 3':
                valor = 5200  # Coloque o valor apropriado aqui
            elif area == 'Aluguer de Casa de 1 piso':
                valor = 8200  # Coloque o valor apropriado aqui
            elif area == 'Aluguer de Casa de 2 pisos':
                valor = 12300  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Aluguer de Imóveis Para Comércio':
            if area == 'Estabelecimento de 0 a 20m2':
                valor = 5200  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 21 a 30m2':
                valor = 7200  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento + 30m2':
                valor = 8200  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 1 piso':
                valor = 12200  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 2 pisos':
                valor = 16300  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Produção ou Distribuição de Electricidade e Água':
            if area == 'Postos de Cobranças de 0-50m2':
                valor = 18720  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 0-50 m2':
                valor = 53944.20  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 51-100 m2':
                valor = 58439.55  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento +100 m2':
                valor = 67329.60  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Comunicações':
            if area == 'Área Ocupada por Antenas':
                valor = 30688.63  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 0-50 m2':
                valor = 46800  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento de 51-100 m2':
                valor = 50581  # Coloque o valor apropriado aqui
            elif area == 'Estabelecimento +100 m2':
                valor = 63180  # Coloque o valor apropriado aqui

        elif sector == 'Categoria de Supermercados':
            if area == '0-50 m2':
                valor = 50544  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 54756  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 63180  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Industrias':
            if area == '0-50 m2':
                valor = 30688.63  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 40014  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 50544  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Estações de Abastecimento de Combustiveis liquídos':
            if area == '0-50 m2':
                valor = 37908  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 40716  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 46800  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Construção':
            if area == '0-50 m2':
                valor = 28080  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 30388.57  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 35063.73  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Pecuária, Agricultura e Pescas':
            if area == '0-50 m2':
                valor = 21577.68  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 23375.82  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 26972.10  # Coloque o valor apropriado aqui
            # Adicione mais opções de área conforme necessário
        elif sector == 'Categoria de Transportes':
            if area == '0-50 m2':
                valor = 21577.68  # Coloque o valor apropriado aqui
            elif area == '51-100 m2':
                valor = 23375.82  # Coloque o valor apropriado aqui
            elif area == '+100 m2':
                valor = 26972.10  # Coloque o valor apropriado aqui
        else:
            valor=0


        # Cria a instância de Propriedade com os dados validados
        estabelecimento = Estabelecimento.objects.create(id_municipe=municipe, bairro=bairro, sector=sector,
                                                         area=area, valor_tae=valor, nome=dados['nome'])
        estabelecimento.save()

        return Response(status=200)




class EstabelecimentoListByMunicipeView(ListAPIView):
    serializer_class = EstabelecimentoSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search')  # Obtém o termo de pesquisa da URL

        queryset = Estabelecimento.objects.all()

        if search_term:
            queryset = queryset.filter(
                Q(id_municipe=search_term) | Q(id_municipe__nr_contribuente=search_term)
            )

        return queryset
