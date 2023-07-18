from django.db.models import Sum
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
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import render
from Municipe.models import Municipe, Bairro
from automovel.views import calcula_iav, AutomovelSerializer
from Propriedade.serializers import*
from impostos.models import Imposto
from rest_framework import status
from django.db import transaction

# Create your views here.
class payIpa(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        try:
            user = request.user
            usuario = User.objects.get(username=user)

            pessoa = Municipe.objects.get(
                nr_contribuente=self.request.data['nr_contribuente']
            )

            bairro = Bairro.objects.get(id=self.request.data['id_bairro'])

            tipo = Imposto.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario
                )

                # Criando o objeto IpaPagamento
                billIpa = IpaPagamento.objects.create(
                    municipe=pessoa,
                    imposto=tipo,
                    pagamento=bill,
                    epoca=self.request.data['epoca']
                )

            serializer = IpaPagamentoSerializer(billIpa)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billIpa' in locals() and billIpa:
                billIpa.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class IpaListView(ListAPIView):
    queryset = IpaPagamento.objects.all()
    serializer_class = IpaPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CheckIpaPagamentoView(APIView):
    def post(self, request, format=None):
        print('start')
        nr_contribuente = request.data.get('nr_contribuente')
        epoca = request.data.get('epoca')

        try:
            municipe = Municipe.objects.get(nr_contribuente=nr_contribuente)
            municipe_s = MunicipeSerializer(municipe).data
            ipa_pagamento = IpaPagamento.objects.get(municipe=municipe, epoca=epoca)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except Municipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IpaPagamento.DoesNotExist:
            return Response({'exists': False, 'data':municipe_s}, status=status.HTTP_200_OK)

class CheckPropPagamentoView(APIView):
    def post(self, request, format=None):
        print(self.request.data)
        id = request.data.get('id')
        epoca = request.data.get('epoca')
        rubrica = request.data.get('rubrica')
        valor=0
        totalPago=0
        saldo=0
        try:
            prop = Propriedade.objects.get(id=id)
            prop_s = PropriedadeSerializer(prop).data
            if(rubrica=='112201'):
                valor= float(prop_s['valor_patrimonial'])*0.02
                print(valor)
            else:
                if(prop_s['tipo']=='Habitacao'):
                    valor= float(prop_s['valor_patrimonial'])*0.004
                else:
                    valor= float(prop_s['valor_patrimonial'])*0.007
            saldo=valor
            prop_pagamento = PropPagamento.objects.filter(propriedade=prop, imposto__rubrica=rubrica,epoca=epoca)
            if(prop_pagamento.exists()):
                valor_total = prop_pagamento.aggregate(Sum('pagamento__valor'))['pagamento__valor__sum']
                if valor_total is None:
                    valor_total = 0
                else:
                    totalPago=valor_total
                    saldo=float(valor)-float(valor_total)

            return Response({'valor':valor,'totalPago':totalPago,'saldo':saldo}, status=status.HTTP_200_OK)
        except Municipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Propriedade.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class payProp(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        try:
            user = request.user
            usuario = User.objects.get(username=user)

            pessoa = Municipe.objects.get(
                nr_contribuente=self.request.data['nr_contribuente']
            )

            bairro = Bairro.objects.get(id=self.request.data['id_bairro'])

            tipo = Imposto.objects.get(rubrica=self.request.data['rubrica'])

            prop=Propriedade.objects.get(id=self.request.data['id_propriedade'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario
                )

                # Criando o objeto IpaPagamento
                billProp = PropPagamento.objects.create(
                    municipe=pessoa,
                    imposto=tipo,
                    pagamento=bill,
                    epoca=self.request.data['epoca'],
                    propriedade=prop
                )

            serializer = PropPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class PropListView(ListAPIView):
    queryset = PropPagamento.objects.all()
    serializer_class = PropPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class CheckIavPagamentoView(APIView):
    def post(self, request, format=None):
        print(self.request.data)
        matricula = request.data.get('matricula')
        epoca = request.data.get('epoca')
        rubrica = request.data.get('rubrica')

        try:
            auto=Automovel.objects.get(matricula=matricula)
            ipa_pagamento = IavPagamento.objects.get(automovel=auto, imposto__rubrica=rubrica, epoca=epoca)
            return Response({'exists': True}, status=status.HTTP_200_OK)
        except Automovel.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IavPagamento.DoesNotExist:
            auto_s=AutomovelSerializer(auto).data
            auto_s['valor']=calcula_iav(AutomovelSerializer(auto))
            return Response({'exists': False, 'data':auto_s}, status=status.HTTP_200_OK)

class payIav(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(self.request.data)
        try:
            user = request.user
            usuario = User.objects.get(username=user)

            pessoa = Municipe.objects.get(
                nr_contribuente=self.request.data['nr_contribuente']
            )

            bairro = Bairro.objects.get(id=self.request.data['id_bairro'])

            tipo = Imposto.objects.get(rubrica=self.request.data['rubrica'])

            auto=Automovel.objects.get(matricula=self.request.data['matricula'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario
                )

                # Criando o objeto IavPagamento
                billIav = IavPagamento.objects.create(
                    municipe=pessoa,
                    imposto=tipo,
                    pagamento=bill,
                    epoca=self.request.data['epoca'],
                    automovel=auto
                )

            serializer = IavPagamentoSerializer(billIav)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billIav' in locals() and billIav:
                billIav.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class IavListView(ListAPIView):
    queryset = IavPagamento.objects.all()
    serializer_class = IavPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]