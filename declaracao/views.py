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
from pagamentos.models import DeclaracaoPagamento
from django.db import transaction

class DeclaracaoCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        taxa=self.request.data['taxa']
        dados=self.request.data['dados']
        id_pay=self.request.data['id']

        user = request.user
        usuario = User.objects.get(username=user)

        #instanciar a declaracao
        pagamento=DeclaracaoPagamento.objects.get(pagamento__id=id_pay)

        if(taxa['destino']=="declaracao-residencia"):
            dcl=DeclaracaoResidencia.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                tempo_residencia=dados['tempo_residencia'],
                razao=dados['destino'],
                user=usuario
            )
        elif(taxa['destino']=="declaracao-pobreza"):
            dcl=DeclaracaoPobreza.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                tempo_residencia=dados['tempo_residencia'],
                razao=dados['destino'],
                user=usuario
            )
        elif(taxa['destino']=="declaracao-coabitacao"):
            dcl=DeclaracaoCoabitacao.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                tempo_residencia=dados['tempo_residencia'],
                conjo=dados['conjo'],
                user=usuario
            )
        elif(taxa['destino']=="declaracao-obito"):
            dcl=DeclaracaoObito.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                data_obito=dados['data_obito'],
                razao_obito=dados['razao_obito'],
                user=usuario
            )
        elif(taxa['destino']=="declaracao-viagem"):
            dcl=DeclaracaoViagem.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                tempo_residencia=dados['tempo_residencia'],
                razao=dados['destino'],
                nome_menor=dados['menor_nome'],
                relacao_menor=dados['relacao_menor'],
                user=usuario
            )
        elif(taxa['destino']=="declaracao-credencial-viagem"):
            dcl=DeclaracaoCredencialViagem.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                veiculo_marca=dados['veiculo_marca'],
                veiculo_matricula=dados['veiculo_matricula'],
                lotacao=dados['lotacao'],
                validade=data_apos_dias(int(dados['validade'])),
                user=usuario
            )
        elif(taxa['destino']=="declaracao-matricial"):
            dcl=DeclaracaoMatricial.objects.create(
                nome=dados['nome'],
                estado_civil=dados['estado_civil'],
                bairro=dados['bairro'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                user=usuario
            )
        #serializar a declaracao
        if isinstance(dcl, DeclaracaoCoabitacao):
            serializer = DeclaracaoCoabitacaoSerializer(dcl)
        elif isinstance(dcl, DeclaracaoPobreza):
            serializer = DeclaracaoPobrezaSerializer(dcl)
        elif isinstance(dcl, DeclaracaoResidencia):
            serializer = DeclaracaoResidenciaSerializer(dcl)
        elif isinstance(dcl, DeclaracaoMatricial):
            serializer = DeclaracaoMatricialSerializer(dcl)
        elif isinstance(dcl, DeclaracaoViagem):
            serializer = DeclaracaoViagemSerializer(dcl)
        elif isinstance(dcl, DeclaracaoCredencialViagem):
            serializer = DeclaracaoCredencialViagemSerializer(dcl)
        elif isinstance(dcl, DeclaracaoObito):
            serializer = DeclaracaoObitoSerializer(dcl)

        return Response(serializer.data)

def data_apos_dias(numero_dias):
    hoje = date.today()
    data_apos = hoje + timedelta(days=numero_dias)
    return data_apos

#lista todo tipo de declaracao declaracaoCoabitacao, etc, que tenham status "Aguardando Aprovacao"
class DeclaracaoListView(ListAPIView):    
    serializer_class = DeclaracaoSerializer
    def get(self, request, format=None):
        todas_declaracoes = (
                list(DeclaracaoCoabitacao.objects.all()) +
                list(DeclaracaoPobreza.objects.all()) +
                list(DeclaracaoResidencia.objects.all()) +
                list(DeclaracaoMatricial.objects.all()) +
                list(DeclaracaoViagem.objects.all()) +
                list(DeclaracaoCredencialViagem.objects.all()) +
                list(DeclaracaoObito.objects.all())
            )
        #filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if declaracao.status == "Aguardando Aprovacao"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, DeclaracaoCoabitacao):
                serializer = DeclaracaoCoabitacaoSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoPobreza):
                serializer = DeclaracaoPobrezaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoResidencia):
                serializer = DeclaracaoResidenciaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoMatricial):
                serializer = DeclaracaoMatricialSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoViagem):
                serializer = DeclaracaoViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoCredencialViagem):
                serializer = DeclaracaoCredencialViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoObito):
                serializer = DeclaracaoObitoSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)
        
        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)

#retorna todas declaracoes de um municipe pelo seu nr_contribuinte
class DeclaracaoMunicipeView(ListAPIView):
    def get(self, request, format=None, **kwargs):
        print("start")
        nr_contribuinte = self.kwargs['nr_contribuente']
        todas_declaracoes = (
                list(DeclaracaoCoabitacao.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoPobreza.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoResidencia.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoMatricial.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoViagem.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoCredencialViagem.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte)) +
                list(DeclaracaoObito.objects.filter(pagamento__municipe__nr_contribuente=nr_contribuinte))
        )

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, DeclaracaoCoabitacao):
                serializer = DeclaracaoCoabitacaoSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoPobreza):
                serializer = DeclaracaoPobrezaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoResidencia):
                serializer = DeclaracaoResidenciaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoMatricial):
                serializer = DeclaracaoMatricialSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoViagem):
                serializer = DeclaracaoViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoCredencialViagem):
                serializer = DeclaracaoCredencialViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoObito):
                serializer = DeclaracaoObitoSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)

        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)


#faca me uma view que recebe o tipo de declaracao e o id da declaracao e mude o status da declaracao para "Aprovado"
class DeclaracaoAprovarView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        tipo = self.request.data['tipo']
        id = self.request.data['id']
        if tipo == "declaracao-coabitacao":
            declaracao = DeclaracaoCoabitacao.objects.get(id=id)
        elif tipo == "declaracao-pobreza":
            declaracao = DeclaracaoPobreza.objects.get(id=id)
        elif tipo == "declaracao-residencia":
            declaracao = DeclaracaoResidencia.objects.get(id=id)
        elif tipo == "declaracao-matricial":
            declaracao = DeclaracaoMatricial.objects.get(id=id)
        elif tipo == "declaracao-viagem":
            declaracao = DeclaracaoViagem.objects.get(id=id)
        elif tipo == "declaracao-credencial-viagem":
            declaracao = DeclaracaoCredencialViagem.objects.get(id=id)
        elif tipo == "declaracao-obito":
            declaracao = DeclaracaoObito.objects.get(id=id)
        else:
            return Response(status=400)

        declaracao.status = "Aprovado"
        #AttributeError: type object 'datetime.timezone' has no attribute 'now'
        declaracao.data_aprovacao = datetime.now()
        declaracao.save()
        return Response(status=200)

class DeclaracaoAprovadaView(ListAPIView):    
    serializer_class = DeclaracaoSerializer
    def get(self, request, format=None):
        todas_declaracoes = (
                list(DeclaracaoCoabitacao.objects.all()) +
                list(DeclaracaoPobreza.objects.all()) +
                list(DeclaracaoResidencia.objects.all()) +
                list(DeclaracaoMatricial.objects.all()) +
                list(DeclaracaoViagem.objects.all()) +
                list(DeclaracaoCredencialViagem.objects.all()) +
                list(DeclaracaoObito.objects.all())
            )
        #filtrar as declaracoes que tenham status "Aguardando Aprovacao"
        todas_declaracoes = [declaracao for declaracao in todas_declaracoes if declaracao.status == "Aprovado"]

        # Ordenar a lista de declarações por data_registo em ordem descendente
        todas_declaracoes = sorted(todas_declaracoes, key=lambda x: x.data_registo, reverse=True)

        # Serializar a lista de declarações usando o serializer apropriado para cada tipo
        serialized_declaracoes = []
        for declaracao in todas_declaracoes:
            if isinstance(declaracao, DeclaracaoCoabitacao):
                serializer = DeclaracaoCoabitacaoSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoPobreza):
                serializer = DeclaracaoPobrezaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoResidencia):
                serializer = DeclaracaoResidenciaSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoMatricial):
                serializer = DeclaracaoMatricialSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoViagem):
                serializer = DeclaracaoViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoCredencialViagem):
                serializer = DeclaracaoCredencialViagemSerializer(declaracao)
            elif isinstance(declaracao, DeclaracaoObito):
                serializer = DeclaracaoObitoSerializer(declaracao)
            else:
                # Trate outros tipos de declaração aqui, se necessário
                continue

            serialized_declaracoes.append(serializer.data)
        
        serialized_declaracoes.reverse()
        return Response(serialized_declaracoes, status=200)


#faca me uma view que recebe o tipo de declaracao e o id da declaracao e mude o status da declaracao para "Rejeitado"
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
                    billProp=DeclaracaoPagamento.objects.get(id=dados['paymentId'])
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
                    billProp = DeclaracaoPagamento.objects.create(
                        municipe=pessoa,
                        taxa=tax,
                        pagamento=bill,
                    )
                    status="Aguardando Pagamento"

                if (taxa['destino'] == "declaracao-residencia"):
                    dcl = DeclaracaoResidencia.objects.create(
                        #o dados['minuta'] e o ficheiro que o usuario enviou, coloca no campo pedido que e um filefield
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-pobreza"):
                    dcl = DeclaracaoPobreza.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-coabitacao"):
                    dcl = DeclaracaoCoabitacao.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-obito"):
                    dcl = DeclaracaoObito.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-viagem"):
                    dcl = DeclaracaoViagem.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-credencial-viagem"):
                    dcl = DeclaracaoCredencialViagem.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                elif (taxa['destino'] == "declaracao-matricial"):
                    dcl = DeclaracaoMatricial.objects.create(
                        pagamento=billProp,
                        pedido=dados["minuta"],
                        status=status
                    )
                dcl.save()

            return Response(status=200)
        except Exception as e:
            # Em caso de erro, remove os objetos criados
            if 'bill' in locals() and bill:
                bill.delete()
            if 'billProp' in locals() and billProp:
                billProp.delete()
            print(e)

            return Response({'error': str(e)}, status=404)
