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
from estabelecimento.models import *
from declaracao.models import *
from urbanizacao.models import *
from planificacao.models import *
from licenciamento.models import *
from taxas.models import *
from rest_framework import status
from django.db import transaction
from datetime import *

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
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        print('start')
        print(self.request.data)
        nr_contribuente = request.data.get('nr_contribuente')
        epoca = request.data.get('epoca')

        try:
            municipe = Municipe.objects.get(nr_contribuente=nr_contribuente)
            municipe_s = MunicipeSerializer(municipe).data
            if(IpaPagamento.objects.filter(municipe=municipe, epoca=epoca, pagamento__isPaid=True).exists()):
                return Response({'exists': True, 'data':municipe_s}, status=200)
            else:
                return Response({'exists': False, 'data': municipe_s}, status=200)
        except Municipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except IpaPagamento.DoesNotExist:
            return Response({'exists': False, 'data':municipe_s}, status=200)

class CheckPropPagamentoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
            prop_pagamento = PropPagamento.objects.filter(propriedade=prop, imposto__rubrica=rubrica,epoca=epoca, pagamento__isPaid=True)
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
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        print(self.request.data)
        matricula = request.data.get('matricula')
        epoca = request.data.get('epoca')
        rubrica = request.data.get('rubrica')

        try:
            auto=Automovel.objects.get(matricula=matricula)
            ipa_pagamento = IavPagamento.objects.get(automovel=auto, imposto__rubrica=rubrica, epoca=epoca, pagamento__isPaid=True)
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
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

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

class CheckTaePagamentoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        print(self.request.data)
        id = request.data.get('id')
        epoca = request.data.get('epoca')
        rubrica = request.data.get('rubrica')
        valor=0
        totalPago=0
        saldo=0
        try:
            prop = Estabelecimento.objects.get(id=id)
            prop_s = EstabelecimentoSerializer(prop).data
            
            valor= float(prop_s['valor_tae'])

            saldo=valor
            tae_pagamento = TaePagamento.objects.filter(estabelecimento=prop, taxa__rubrica=rubrica,epoca=epoca)
            if(tae_pagamento.exists()):
                valor_total = tae_pagamento.aggregate(Sum('pagamento__valor'))['pagamento__valor__sum']
                if valor_total is None:
                    valor_total = 0
                else:
                    totalPago=valor_total
                    saldo=float(valor)-float(valor_total)
            return Response({'valor':valor,'totalPago':totalPago,'saldo':saldo}, status=status.HTTP_200_OK)
        except Municipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Estabelecimento.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class payTae(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            prop=Estabelecimento.objects.get(id=self.request.data['id_estabelecimento'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = TaePagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                    epoca=self.request.data['epoca'],
                    estabelecimento=prop
                )

            serializer = TaePagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class TaeListView(ListAPIView):
    queryset = TaePagamento.objects.all()
    serializer_class = TaePagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class payDeclaracao(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = DeclaracaoPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                )

            serializer = DeclaracaoPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class DeclaracaoListView(ListAPIView):
    queryset = DeclaracaoPagamento.objects.all()
    serializer_class = DeclaracaoPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DeclaracaoCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        idDcl = request.data.get('id')
        try:
            dcl_pay = DeclaracaoPagamento.objects.get(pagamento__id=idDcl)
            dcl_s=DeclaracaoPagamentoSerializer(dcl_pay).data
            # Verificar o tipo da declaração associada e obter o objeto concreto
            if hasattr(dcl_pay, 'declaracaocoabitacao'):
                declaracao_associada = dcl_pay.declaracaocoabitacao
            elif hasattr(dcl_pay, 'declaracaopobreza'):
                declaracao_associada = dcl_pay.declaracaopobreza
            elif hasattr(dcl_pay, 'declaracaoresidencia'):
                declaracao_associada = dcl_pay.declaracaoresidencia
            elif hasattr(dcl_pay, 'declaracaomatricial'):
                declaracao_associada = dcl_pay.declaracaomatricial
            elif hasattr(dcl_pay, 'declaracaoviagem'):
                declaracao_associada = dcl_pay.declaracaoviagem
            elif hasattr(dcl_pay, 'declaracaocredencialviagem'):
                declaracao_associada = dcl_pay.declaracaocredencialviagem
            elif hasattr(dcl_pay, 'declaracaoobito'):
                declaracao_associada = dcl_pay.declaracaoobito
            else:
                # Caso a declaração associada não corresponda a nenhum tipo conhecido
                return Response({'exists': False, 'pay': dcl_s['taxa']}, status=status.HTTP_200_OK)
            # Obter os dados serializados da declaração associada
            return Response({'exists': True}, status=status.HTTP_200_OK)

        except DeclaracaoPagamento.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class payUrb(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            prop=Propriedade.objects.get(id=self.request.data['id_propriedade'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = UrbPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                    propriedade=prop
                )

            serializer = UrbPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class UrbListView(ListAPIView):
    queryset = UrbPagamento.objects.all()
    serializer_class = UrbPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class payPub(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = PubPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                    unidade=self.request.data['unit']
                )

            serializer = PubPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class PubListView(ListAPIView):
    queryset = PubPagamento.objects.all()
    serializer_class = PubPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class payTrans(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = TransPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                )

            serializer = TransPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class TransListView(ListAPIView):
    queryset = TransPagamento.objects.all()
    serializer_class = TransPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ListImpostos(APIView):
    def get(self, request, format=None):
        ipa_pagamentos=IpaPagamento.objects.all()	
        prop_pagamentos=PropPagamento.objects.all()
        iav_pagamentos=IavPagamento.objects.all()

        #serializers
        ipa_serializer=IpaPagamentoSerializer(ipa_pagamentos, many=True)
        prop_serializer=PropPagamentoSerializer(prop_pagamentos, many=True)
        iav_serializer=IavPagamentoSerializer(iav_pagamentos, many=True)

        #junta em uma lista e ordena por pagamento.data
        lista=ipa_serializer.data+prop_serializer.data+iav_serializer.data
        lista.sort(key=lambda x: x['pagamento']['data'])

        #retorne o response
        return Response(lista, status=status.HTTP_200_OK)

class ListTaxas(APIView):
    def get(self, request, format=None):
        tae_pagamentos=TaePagamento.objects.all()
        urb_pagamentos=UrbPagamento.objects.all()
        decl_pagamentos=DeclaracaoPagamento.objects.all()
        pub_pagamentos=PubPagamento.objects.all()
        trans_pagamentos=TransPagamento.objects.all()
        residual_pagamentos=ResidualPagamento.objects.all()
        mercado_pagamentos=MercadoPagamento.objects.all()
        generico_pagamentos=GenericoPagamento.objects.all()
        #serializers
        tae_serializer=TaePagamentoSerializer(tae_pagamentos, many=True)
        urb_serializer=UrbPagamentoSerializer(urb_pagamentos, many=True)
        decl_serializer=DeclaracaoPagamentoSerializer(decl_pagamentos, many=True)
        pub_serializer=PubPagamentoSerializer(pub_pagamentos, many=True)
        trans_serializers=TransPagamentoSerializer(trans_pagamentos, many=True)
        residual_serializers=ResidualPagamentoSerializer(residual_pagamentos, many=True)
        mercado_serializers=MercadoPagamentoSerializer(mercado_pagamentos, many=True)
        generico_serializer=GenericoPagamentoSerializer(generico_pagamentos, many=True)
        #junta em uma lista e ordena por pagamento.data
        lista=tae_serializer.data+generico_serializer.data+urb_serializer.data+decl_serializer.data+pub_serializer.data+trans_serializers.data+residual_serializers.data+mercado_serializers.data
        lista.sort(key=lambda x: x['pagamento']['data'])

        #retorne o response
        return Response(lista, status=status.HTTP_200_OK)

class UrbanizacaoCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        idUrb = request.data.get('id')
        try:
            urb_pay = UrbPagamento.objects.get(pagamento__id=idUrb)
            urb_s= UrbPagamentoSerializer(urb_pay).data
            # Verificar o tipo da declaração associada e obter o objeto concreto
            if hasattr(urb_pay, 'licensaduat'):
                licensa_associada = urb_pay.licensaduat
            else:
                # Caso a declaração associada não corresponda a nenhum tipo conhecido
                return Response({'exists': False, 'dados': urb_s}, status=status.HTTP_200_OK)
            # Obter os dados serializados da declaração associada
            return Response({'exists': True}, status=status.HTTP_200_OK)

        except UrbPagamento.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PlanificacaoCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        idPlan = request.data.get('id')
        try:
            plan_pay = TransPagamento.objects.get(pagamento__id=idPlan)
            plan_s= TransPagamentoSerializer(plan_pay).data
            # Verificar o tipo da declaração associada e obter o objeto concreto
            if LicensaTransporte.objects.filter(pagamento=plan_pay).exists() or LicensaTransporte.objects.filter(pagamento=plan_pay).exists():
                pass
            else:
                # Caso a declaração associada não corresponda a nenhum tipo conhecido
                return Response({'exists': False, 'dados': plan_s}, status=status.HTTP_200_OK)
            # Obter os dados serializados da declaração associada
            return Response({'exists': True}, status=status.HTTP_200_OK)

        except TransPagamento.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class payResidual(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = ResidualPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                )

            serializer = ResidualPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class ResidualListView(ListAPIView):
    queryset = ResidualPagamento.objects.all()
    serializer_class = ResidualPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class payMercado(CreateAPIView):
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

            mercado=Mercado.objects.get(id=self.request.data['id_mercado'])

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = MercadoPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    mercado=mercado,
                    pagamento=bill,
                )

            serializer = MercadoPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class MercadoListView(ListAPIView):
    queryset = MercadoPagamento.objects.all()
    serializer_class = MercadoPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class payGenerico(CreateAPIView):
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

            tipo = Taxa.objects.get(rubrica=self.request.data['rubrica'])

            with transaction.atomic():  # Inicia uma transação

                # Criando o objeto Pagamento
                bill = Pagamento.objects.create(
                    bairro=bairro,
                    valor=self.request.data['valor'],
                    user=usuario,
                    metodo=self.request.data['metodo']
                )

                if self.request.data['metodo'] == None:
                    bill.isPaid=False
                    bill.save()
                else:
                    bill.isPaid = True
                    bill.save()

                # Criando o objeto IpaPagamento
                billProp = GenericoPagamento.objects.create(
                    municipe=pessoa,
                    taxa=tipo,
                    pagamento=bill,
                )

            serializer = GenericoPagamentoSerializer(billProp)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()

            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 

class GenericoListView(ListAPIView):
    queryset = GenericoPagamento.objects.all()
    serializer_class = GenericoPagamentoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class MunicipePagamentos(APIView):
    def get(self, request, format=None, **kwargs):
        municipe=Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuinte'])

        ipa_pagamentos=IpaPagamento.objects.filter(municipe=municipe)
        prop_pagamentos=PropPagamento.objects.filter(municipe=municipe)
        iav_pagamentos=IavPagamento.objects.filter(municipe=municipe)
        tae_pagamentos=TaePagamento.objects.filter(municipe=municipe)
        urb_pagamentos=UrbPagamento.objects.filter(municipe=municipe)
        decl_pagamentos=DeclaracaoPagamento.objects.filter(municipe=municipe)
        pub_pagamentos=PubPagamento.objects.filter(municipe=municipe)
        trans_pagamentos=TransPagamento.objects.filter(municipe=municipe)
        residual_pagamentos=ResidualPagamento.objects.filter(municipe=municipe)
        mercado_pagamentos=MercadoPagamento.objects.filter(municipe=municipe)
        generico_pagamentos=GenericoPagamento.objects.filter(municipe=municipe)
        #serializers
        ipa_serializer=IpaPagamentoSerializer(ipa_pagamentos, many=True)
        prop_serializer=PropPagamentoSerializer(prop_pagamentos, many=True)
        iav_serializer=IavPagamentoSerializer(iav_pagamentos, many=True)
        tae_serializer=TaePagamentoSerializer(tae_pagamentos, many=True)
        urb_serializer=UrbPagamentoSerializer(urb_pagamentos, many=True)
        decl_serializer=DeclaracaoPagamentoSerializer(decl_pagamentos, many=True)
        pub_serializer=PubPagamentoSerializer(pub_pagamentos, many=True)
        trans_serializers=TransPagamentoSerializer(trans_pagamentos, many=True)
        residual_serializers=ResidualPagamentoSerializer(residual_pagamentos, many=True)
        mercado_serializers=MercadoPagamentoSerializer(mercado_pagamentos, many=True)
        generico_serializer=GenericoPagamentoSerializer(generico_pagamentos, many=True)
        #junta em uma lista e ordena por pagamento.data
        lista=tae_serializer.data+generico_serializer.data+urb_serializer.data+decl_serializer.data+pub_serializer.data+trans_serializers.data+residual_serializers.data+mercado_serializers.data+iav_serializer.data+ipa_serializer.data+prop_serializer.data
        lista.sort(key=lambda x: x['pagamento']['data'])

        print(lista)
        #retorne o response
        return Response(lista, status=status.HTTP_200_OK)

class LicenciamentoCheckView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        idPlan = request.data.get('id')
        try:
            plan_pay = GenericoPagamento.objects.get(pagamento__id=idPlan, taxa__destino="ae-lic")
            plan_s= GenericoPagamentoSerializer(plan_pay).data
            # Verificar o tipo da declaração associada e obter o objeto concreto
            if LicensaAE.objects.filter(pagamento=plan_pay).exists():
                pass
            else:
                # Caso a declaração associada não corresponda a nenhum tipo conhecido
                return Response({'exists': False, 'dados': plan_s}, status=status.HTTP_200_OK)
            # Obter os dados serializados da declaração associada
            return Response({'exists': True}, status=status.HTTP_200_OK)

        except GenericoPagamento.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GuiaMunicipe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        municipe=Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuinte'])
        municipe_s=MunicipeSerializer(municipe).data
        ipa_pagamentos=IpaPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        prop_pagamentos=PropPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        iav_pagamentos=IavPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        tae_pagamentos=TaePagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        urb_pagamentos=UrbPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        decl_pagamentos=DeclaracaoPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        pub_pagamentos=PubPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        trans_pagamentos=TransPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        residual_pagamentos=ResidualPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        mercado_pagamentos=MercadoPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        generico_pagamentos=GenericoPagamento.objects.filter(municipe=municipe, pagamento__isPaid=False)
        #serializers
        ipa_serializer=IpaPagamentoSerializer(ipa_pagamentos, many=True)
        prop_serializer=PropPagamentoSerializer(prop_pagamentos, many=True)
        iav_serializer=IavPagamentoSerializer(iav_pagamentos, many=True)
        tae_serializer=TaePagamentoSerializer(tae_pagamentos, many=True)
        urb_serializer=UrbPagamentoSerializer(urb_pagamentos, many=True)
        decl_serializer=DeclaracaoPagamentoSerializer(decl_pagamentos, many=True)
        pub_serializer=PubPagamentoSerializer(pub_pagamentos, many=True)
        trans_serializers=TransPagamentoSerializer(trans_pagamentos, many=True)
        residual_serializers=ResidualPagamentoSerializer(residual_pagamentos, many=True)
        mercado_serializers=MercadoPagamentoSerializer(mercado_pagamentos, many=True)
        generico_serializer=GenericoPagamentoSerializer(generico_pagamentos, many=True)
        #junta em uma lista e ordena por pagamento.data
        lista=tae_serializer.data+generico_serializer.data+urb_serializer.data+decl_serializer.data+pub_serializer.data+trans_serializers.data+residual_serializers.data+mercado_serializers.data+iav_serializer.data+ipa_serializer.data+prop_serializer.data
        lista.sort(key=lambda x: x['pagamento']['data'])

        print(lista)
        #retorne o response
        return Response(data={'municipe':municipe_s, 'lista':lista}, status=status.HTTP_200_OK)


#quero uma view quer recebe o id  do pagamento e muda o isPaid para true e faz update do user, suponha que receba mais de um pagamento
class ConfirmarPagamento(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        pays=request.data.get('pays')
        user = request.user
        usuario = User.objects.get(username=user)
        for pay in pays:
            try:
                pagamento=Pagamento.objects.get(id=pay)
                pagamento.isPaid=True
                pagamento.user=usuario
                pagamento.data=datetime.now()
                pagamento.save()
            except Pagamento.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

class RelatorioCaixa(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        user = request.user
        usuario = User.objects.get(username=user)

        ipa_pagamentos=IpaPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        prop_pagamentos=PropPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        iav_pagamentos=IavPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        tae_pagamentos=TaePagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        urb_pagamentos=UrbPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        decl_pagamentos=DeclaracaoPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        pub_pagamentos=PubPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        trans_pagamentos=TransPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        residual_pagamentos=ResidualPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        mercado_pagamentos=MercadoPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        generico_pagamentos=GenericoPagamento.objects.filter(pagamento__isPaid=True, pagamento__user=usuario)
        #serializers
        ipa_serializer=IpaPagamentoSerializer(ipa_pagamentos, many=True)
        prop_serializer=PropPagamentoSerializer(prop_pagamentos, many=True)
        iav_serializer=IavPagamentoSerializer(iav_pagamentos, many=True)
        tae_serializer=TaePagamentoSerializer(tae_pagamentos, many=True)
        urb_serializer=UrbPagamentoSerializer(urb_pagamentos, many=True)
        decl_serializer=DeclaracaoPagamentoSerializer(decl_pagamentos, many=True)
        pub_serializer=PubPagamentoSerializer(pub_pagamentos, many=True)
        trans_serializers=TransPagamentoSerializer(trans_pagamentos, many=True)
        residual_serializers=ResidualPagamentoSerializer(residual_pagamentos, many=True)
        mercado_serializers=MercadoPagamentoSerializer(mercado_pagamentos, many=True)
        generico_serializer=GenericoPagamentoSerializer(generico_pagamentos, many=True)
        #junta em uma lista e ordena por pagamento.data
        lista=tae_serializer.data+generico_serializer.data+urb_serializer.data+decl_serializer.data+pub_serializer.data+trans_serializers.data+residual_serializers.data+mercado_serializers.data+iav_serializer.data+ipa_serializer.data+prop_serializer.data
        lista.sort(key=lambda x: x['pagamento']['data'])

        print(lista)
        #retorne o response
        return Response(data={'lista':lista}, status=status.HTTP_200_OK)

#com base no nr_contribuinte, retorna filtra os DeclaraçãoPagamento em que o pagamento.isPaid=True
class DeclaracaoPagamentoMunicipe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        print(self.kwargs['nr_contribuinte'])
        print(self.kwargs['rubrica'])
        municipe=Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuinte'])
        rubrica=self.kwargs['rubrica']
        municipe_s=MunicipeSerializer(municipe).data
        decl_pagamentos=DeclaracaoPagamento.objects.filter(municipe=municipe, pagamento__isPaid=True)

        #pega cada um dos pagamentos e verifica se existe uma declaração associada, se nao existir retorna o response do pagamento serializado
        lista=[]
        for decl in decl_pagamentos:
            # Verificar o tipo da declaração associada e obter o objeto concreto
            if hasattr(decl, 'declaracaopobreza'):
                declaracao_associada = decl.declaracaopobreza
            elif hasattr(decl, 'declaracaoresidencia'):
                declaracao_associada = decl.declaracaoresidencia
            elif hasattr(decl, 'declaracaomatricial'):
                declaracao_associada = decl.declaracaomatricial
            elif hasattr(decl, 'declaracaoviagem'):
                declaracao_associada = decl.declaracaoviagem
            elif hasattr(decl, 'declaracaocredencialviagem'):
                declaracao_associada = decl.declaracaocredencialviagem
            elif hasattr(decl, 'declaracaoobito'):
                declaracao_associada = decl.declaracaoobito
            else:
                # Caso a declaração associada não corresponda a nenhum tipo conhecido
                if(decl.taxa.rubrica==rubrica):
                    return Response({'exists': True, 'id':decl.id}, status=status.HTTP_200_OK)
                else:
                    pass

        return Response(data={'exists':False}, status=status.HTTP_200_OK)

class LicensaPagamentoMunicipe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        municipe=Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuinte'])
        rubrica = self.kwargs['rubrica']
        municipe_s=MunicipeSerializer(municipe).data
        decl_pagamentos=GenericoPagamento.objects.filter(municipe=municipe, pagamento__isPaid=True, taxa__destino="ae-lic")

        #pega cada um dos pagamentos e verifica se existe uma declaração associada, se nao existir retorna o response do pagamento serializado
        lista=[]
        for decl in decl_pagamentos:
            if LicensaAE.objects.filter(pagamento=decl).exists():
                pass
            else:
                if (decl.taxa.rubrica == rubrica):
                    return Response({'exists': True, 'id': decl.id}, status=status.HTTP_200_OK)
                else:
                    pass
        return Response(data={'exists':False}, status=status.HTTP_200_OK)

class PlanificacaoPagamentoMunicipe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        print(self.kwargs['rubrica'])
        municipe=Municipe.objects.get(nr_contribuente=self.kwargs['nr_contribuinte'])
        rubrica = self.kwargs['rubrica']
        municipe_s=MunicipeSerializer(municipe).data
        decl_pagamentos=TransPagamento.objects.filter(municipe=municipe, pagamento__isPaid=True)
        #pega cada um dos pagamentos e verifica se existe uma declaração associada, se nao existir retorna o response do pagamento serializado
        lista=[]
        for decl in decl_pagamentos:
            print(decl.taxa.rubrica)
            print(rubrica)
            if LicensaTransporte.objects.filter(pagamento=decl).exists():
                pass
            if LicensaAgua.objects.filter(pagamento=decl).exists():
                pass
            else:
                if (decl.taxa.rubrica == rubrica):
                    return Response({'exists': True, 'id': decl.id}, status=status.HTTP_200_OK)
                else:
                    pass
        return Response(data={'exists':False}, status=status.HTTP_200_OK)
