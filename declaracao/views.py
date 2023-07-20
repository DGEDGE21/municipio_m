from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from .models import *
from .serializers import *
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

class DeclaracaoCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        taxa=self.request.data['taxa']
        dados=self.request.data['dados']
        id_pay=self.request.data['id']

        #instanciar a declaracao
        pagamento=DeclaracaoPagamento.objects.get(id=id_pay)

        if(taxa['destino']=="declaracao-residencia"):
            dcl=DeclaracaoResidencia.objects.create(
                nome=dados['nome'],
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
            )
        elif(taxa['destino']=="declaracao-pobreza"):
            dcl=DeclaracaoPobreza.objects.create(
                nome=dados['nome'],
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
            )
        elif(taxa['destino']=="declaracao-coabitacao"):
            dcl=DeclaracaoCoabitacao.objects.create(
                nome=dados['nome'],
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
            )
        elif(taxa['destino']=="declaracao-obito"):
            dcl=DeclaracaoObito.objects.create(
                nome=dados['nome'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
                data_obito=dados['data_obito'],
                razao_obito=dados['razao_obito']
            )
        elif(taxa['destino']=="declaracao-viagem"):
            dcl=DeclaracaoViagem.objects.create(
                nome=dados['nome'],
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
            )
        elif(taxa['destino']=="declaracao-credencial-viagem"):
            dcl=DeclaracaoCredencialViagem.objects.create(
                nome=dados['nome'],
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
                validade=data_apos_dias(int(dados['validade']))
            )
        elif(taxa['destino']=="declaracao-matricial"):
            dcl=DeclaracaoMatricial.objects.create(
                nome=dados['nome'],
                pai=dados['nome_pai'],
                mae=dados['nome_mae'],
                naturalidade=dados['naturalidade'],
                bi=dados['bi'],
                bi_emissao=dados['bi_emissao'],
                bi_local=dados['bi_local'],
                pagamento=pagamento,
                data_nasc=dados['data_nasc'],
            )
        return Response(status=200)

def data_apos_dias(numero_dias):
    hoje = date.today()
    data_apos = hoje + timedelta(days=numero_dias)
    return data_apos