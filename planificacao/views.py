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
from pagamentos.models import TransPagamento
from django.db import transaction

class LicensaCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        id = request.data['id']
        dados = request.data['dados']
        user = request.user
        usuario = User.objects.get(username=user)

        urb = TransPagamento.objects.get(pagamento__id=id)
        destino = urb.taxa.destino
        print(urb.taxa.destino)

        if destino == 'trans-agua-lic':
            dcl = LicensaAgua.objects.create(
                pagamento=urb,
                user=usuario,
                bairro=dados['bairro'],
                quarteirao=dados['quarteirao'],
                nr_casa=dados['nr_casa']
            )
        elif (destino == 'trans-lic' or destino == 'trans-tax-lic'):
            try:
                rota = dados['rota']
            except:
                rota = 'none'
            auto=Automovel.objects.get(id=dados['id_automovel'])
            dcl = LicensaTransporte.objects.create(
                veiculo=auto,
                rota=rota,
                pagamento=urb,
                user=usuario
            )

        if isinstance(dcl, LicensaAgua):
            serializer = LicensaAguaSerializer(dcl)
        elif isinstance(dcl, LicensaTransporte):
            serializer = LicensaTransporteSerializer(dcl)
        print(serializer.data)
        return Response(serializer.data)


class LicensaListView(ListAPIView):

    def get(self, request, format=None):
        todas_declaracoes = (
                list(LicensaAgua.objects.all()) +
                list(LicensaTransporte.objects.all())
        )
        # filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if
                             declaracao.status == "Aguardando Aprovacao"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, LicensaAgua):
                serializer = LicensaAguaSerializer(declaracao)
            elif isinstance(declaracao, LicensaTransporte):
                serializer = LicensaTransporteSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)

        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)

class LicensaAprovedView(ListAPIView):
    def get(self, request, format=None):
        todas_declaracoes = (
                list(LicensaAgua.objects.all()) +
                list(LicensaTransporte.objects.all())
            )
        #filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if declaracao.status == "Aprovado"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, LicensaAgua):
                serializer = LicensaAguaSerializer(declaracao)
            elif isinstance(declaracao, LicensaTransporte):
                serializer = LicensaTransporteSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)
        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)

class LicensaAprovarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        destino = self.request.data['destino']
        id = self.request.data['id']
        if destino == "trans-agua-lic":
            licensa = LicensaAgua.objects.get(id=id)
        elif (destino == "trans-lic" or destino=='trans-tax-lic'):
            licensa = LicensaTransporte.objects.get(id=id)
        else:
            return Response(status=400)

        licensa.status = "Aprovado"
        #AttributeError: type object 'datetime.timezone' has no attribute 'now'
        licensa.data_aprovacao = datetime.now()
        licensa.save()
        return Response(status=200)

class NovoPedido(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        dados=self.request.data
        print(dados)

        try:
            user = request.user

            usuario = User.objects.get(username=user)

            pessoa = Municipe.objects.get(
                nr_contribuente=dados['nca']
            )

            tax = Taxa.objects.get(rubrica=dados['rubrica'])
            taxa=TaxaSerializer(tax).data
            with transaction.atomic():  # Inicia uma transação

                if(dados['status']=="paid"):
                    billProp=TransPagamento.objects.get(id=dados['paymentId'])
                    status="Em Processo"
                else:
                    # Criando o objeto Pagamento
                    bill = Pagamento.objects.create(
                        bairro=pessoa.bairro,
                        valor=float(taxa['valor']),
                        user=usuario,
                        metodo=None,
                        isPaid=False
                    )
                    bill.save()
                    # Criando o objeto DclPagamento
                    billProp = TransPagamento.objects.create(
                        municipe=pessoa,
                        taxa=tax,
                        pagamento=bill,
                    )
                    status="Aguardando Pagamento"

                if(tax.rubrica=='tr11' or tax.rubrica=='tr15'):
                    dcl = LicensaTransporte.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                    dcl.save()
                elif(tax.rubrica=='tr13'):
                    dcl = LicensaAgua.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                    dcl.save()
                else:
                    return Response(status=400)
            return Response(status=200)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()
            print(e)

            return Response({'error': str(e)}, status=404)
