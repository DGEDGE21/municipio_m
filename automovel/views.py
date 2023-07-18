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

class AutomovelCreateView(CreateAPIView):
    serializer_class = AutomovelSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class AutomovelDetailView(RetrieveAPIView):
    queryset = Automovel.objects.all()
    serializer_class = AutomovelSerializer
    lookup_field = 'matricula'

class AutomovelListByMunicipeView(ListAPIView):
    serializer_class = AutomovelSerializer

    def get_queryset(self):
        id_municipe = self.kwargs['id_municipe']  # Obtém o idMunicipe passado na URL
        queryset = Automovel.objects.filter(id_municipe=id_municipe)  # Filtra os veículos pelo idMunicipe
        return queryset

class AutomovelGrupoCreateView(APIView):
    def post(self, request, format=None):
        data = request.data  # Array com os dados para cadastrar

        for item in data:
            grupo = item.get('grupo')
            cilindara_inicialg = item.get('cilindara_inicialg')
            cilindara_finalg = item.get('cilindara_finalg')
            cilindara_inicialdi = item.get('cilindara_inicialdi')
            cilindara_finaldi = item.get('cilindara_finaldi')
            cilindara_inicialvol = item.get('cilindara_inicialvol')
            cilindara_finaldvol = item.get('cilindara_finaldvol')

            automovel_grupo = Automovel_Grupo.objects.create(
                grupo=grupo,
                cilindara_inicialg=cilindara_inicialg,
                cilindara_finalg=cilindara_finalg,
                cilindara_inicialdi=cilindara_inicialdi,
                cilindara_finaldi=cilindara_finaldi,
                cilindara_inicialvol=cilindara_inicialvol,
                cilindara_finaldvol=cilindara_finaldvol
            )
            # Faça outras operações necessárias com o objeto automovel_grupo, se necessário

        return Response(status=201)
    
class AutomovelGrupoEscalaoCreateView(APIView):
    def post(self, request, format=None):
        data = request.data  # Array com os dados para cadastrar

        for item in data:
            primeiro_escalao = item.get('primeiro_escalao')
            segundo_escalao = item.get('segundo_escalao')
            terceiro_escalao = item.get('Terceiro_escalao')
            grupo_id = item.get('grupo')

            grupo = Automovel_Grupo.objects.get(idGrupo=grupo_id)

            automovel_grupo_escalao = Automovel_Grupo_Escalao.objects.create(
                primeiro_escalao=primeiro_escalao,
                segundo_escalao=segundo_escalao,
                Terceiro_escalao=terceiro_escalao,
                grupo=grupo
            )
            # Faça outras operações necessárias com o objeto automovel_grupo_escalao, se necessário

        return Response(status=201)


#Metodo Para Calcular Valor do IAV
def calcula_iav(serializado):
    if serializado.data['tipo'] == 'Ligeiro':
        if serializado.data['combustivel'] == 'Gasolina':
            cc = int(serializado.data['cilindrada'])
            diferenca = int(localtime().tm_year) - int(serializado.data['ano_fabrico'])
            serializado_s = serializado.data
            if cc <= 1000:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="A"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 200
                if diferenca > 6 and diferenca <= 12:
                    valor = 100
                if diferenca > 12 and diferenca < 25:
                    valor = 50
                if diferenca >= 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 1000 and cc <= 1300:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="B"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 400
                if diferenca > 6 and diferenca <= 12:
                    valor = 200
                if diferenca > 12 and diferenca <= 25:
                    valor = 100
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 1300 and cc <= 1750:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="C"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 600
                if diferenca > 6 and diferenca <= 12:
                    valor = 300
                if diferenca > 12 and diferenca <= 25:
                    valor = 150
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 1750 and cc <= 2600:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="D"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 1600
                if diferenca > 6 and diferenca <= 12:
                    valor = 800
                if diferenca > 12 and diferenca <= 25:
                    valor = 400
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 2600 and cc <= 3500:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="E"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 2400
                if diferenca > 6 and diferenca <= 12:
                    valor = 1200
                if diferenca > 12 and diferenca <= 25:
                    valor = 600
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 3500:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="F"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 4400
                if diferenca > 6 and diferenca <= 12:
                    valor = 2200
                if diferenca > 12 and diferenca < 25:
                    valor = 1100
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
        if serializado.data['combustivel'] == 'Outro':
            cc = int(serializado.data['cilindrada'])
            diferenca = int(localtime().tm_year) - int(serializado.data['ano_fabrico'])
            serializado_s = serializado.data
            if cc <= 1500:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="A"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 200
                if diferenca > 6 and diferenca <= 12:
                    valor = 100
                if diferenca > 12 and diferenca <= 25:
                    valor = 50
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 1500 and cc <= 2000:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="B"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 400
                if diferenca > 6 and diferenca <= 12:
                    valor = 200
                if diferenca > 12 and diferenca <= 25:
                    valor = 100
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 2000 and cc <= 3000:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="C"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 600
                if diferenca > 6 and diferenca <= 12:
                    valor = 300
                if diferenca > 12 and diferenca <= 25:
                    valor = 150
                if diferenca > 25:
                    valor = 0
                serializado_s.update({"valor": valor})
            if cc > 3000:
                escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="F"))
                escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
                if diferenca <= 6:
                    valor = 1600
                if diferenca > 6 and diferenca <= 12:
                    valor = 800
                if diferenca > 12 and diferenca <= 25:
                    valor = 400
                if diferenca > 25:
                    valor = 0

                serializado_s.update({"valor": valor})
    if serializado.data['tipo'] == 'Pesado de Carga':
        cc = int(serializado.data['capacidade_carga'])
        diferenca = int(localtime().tm_year) - int(serializado.data['ano_fabrico'])
        serializado_s = serializado.data
        if cc <= 5000:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="G"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 180
            if diferenca > 6 and diferenca <= 12:
                valor = 120

            if diferenca > 12 and diferenca <= 25:
                valor = 60
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 5000 and cc <= 10000:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="H"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 360
            if diferenca > 6 and diferenca <= 12:
                valor = 240

            if diferenca > 12 and diferenca <= 25:
                valor = 120
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 10000 and cc <= 16000:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="I"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 1080
            if diferenca > 6 and diferenca <= 12:
                valor = 720
            if diferenca > 12 and diferenca <= 25:
                valor = 360
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 16000:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="J"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 2160
            if diferenca > 6 and diferenca <= 12:
                valor = 1440
            if diferenca > 12 and diferenca <= 25:
                valor = 720
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
    if serializado.data['tipo'] == 'Pesado de passageiros':
        cc = int(serializado.data['lotacao'])
        diferenca = int(localtime().tm_year) - int(serializado.data['ano_fabrico'])
        serializado_s = serializado.data
        if cc >= 10 and cc <= 25:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="K"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 180
            if diferenca > 6 and diferenca <= 12:
                valor = 120
            if diferenca > 12 and diferenca <= 25:
                valor = 60
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 25 and cc <= 40:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="L"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 360
            if diferenca > 6 and diferenca <= 12:
                valor = 240
            if diferenca > 12 and diferenca <= 25:
                valor = 120
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 40 and cc <= 70:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="M"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 1080
            if diferenca > 6 and diferenca <= 12:
                valor = 720
            if diferenca > 12 and diferenca <= 25:
                valor = 360
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
        if cc > 70:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="N"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 6:
                valor = 2160
            if diferenca > 6 and diferenca <= 12:
                valor = 1440
            if diferenca > 12 and diferenca <= 25:
                valor = 720
            if diferenca > 25:
                valor = 0

            serializado_s.update({"valor": valor})
    if serializado.data['tipo'] == 'Motociclo':
        cc = int(serializado.data['cilindrada'])
        diferenca = int(localtime().tm_year) - int(serializado.data['ano_fabrico'])
        serializado_s = serializado.data
        if cc <= 50:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="MA"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 5:
                valor = escaloes_s['primeiro_escalao']
            if diferenca > 5 and diferenca <= 10:
                valor = escaloes_s['segundo_escalao']
            if diferenca > 10 and diferenca < 15:
                valor = escaloes_s['Terceiro_escalao']
            if diferenca > 14:
                valor = 0
            serializado_s.update({"valor": valor})
        if cc > 50 and cc <= 100:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="MB"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 5:
                valor = escaloes_s['primeiro_escalao']
            if diferenca > 5 and diferenca <= 10:
                valor = escaloes_s['segundo_escalao']
            if diferenca > 10 and diferenca < 15:
                valor = escaloes_s['Terceiro_escalao']
            if diferenca > 14:
                valor = 0
            serializado_s.update({"valor": valor})
        if cc > 100 and cc <= 500:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="MC"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 5:
                valor = escaloes_s['primeiro_escalao']
            if diferenca > 5 and diferenca <= 10:
                valor = escaloes_s['segundo_escalao']
            if diferenca > 10 and diferenca < 15:
                valor = escaloes_s['Terceiro_escalao']
            if diferenca > 14:
                valor = 0
            serializado_s.update({"valor": valor})
        if cc > 500:
            escaloes = Automovel_Grupo_Escalao.objects.get(grupo=Automovel_Grupo.objects.get(grupo="MD"))
            escaloes_s = Automovel_Grupo_Escalao_Serializado(escaloes).data
            if diferenca <= 5:
                valor = escaloes_s['primeiro_escalao']
            if diferenca > 5 and diferenca <= 10:
                valor = escaloes_s['segundo_escalao']
            if diferenca > 10 and diferenca < 15:
                valor = escaloes_s['Terceiro_escalao']
            if diferenca > 14:
                valor = 0
            serializado_s.update({"valor": valor})
    if serializado.data['natureza'] == 'Estado':
        valor = 0
        serializado_s.update({"valor": valor})

    #calculo de Multas
    var=int(serializado_s['valor'])
    actual=date.today()
    if var>0:
        #limite de 1 de abril ate 30 de abril
        dtLim1=date(year=int(localtime().tm_year),month=4, day=1)
        dtLim2=date(year=int(localtime().tm_year),month=4, day=30)

        #limite de 1 de maio ate 31 de Dezembro
        dtLim3=date(year=int(localtime().tm_year),month=5, day=1)
        dtLim4=date(year=int(localtime().tm_year),month=12, day=31)

        if actual>=dtLim1 and actual<=dtLim2:
            serializado_s.update({'valor': int(serializado_s['valor'])*1.5})
        elif actual>=dtLim3 and actual<=dtLim4:
            serializado_s.update({'valor': int(serializado_s['valor'])*3})
            
    elif var==0 and serializado.data['natureza'] != 'Estado':
        #limite de 1 de abril ate 30 de abril
        dtLim1=date(year=int(localtime().tm_year),month=4, day=1)
        dtLim2=date(year=int(localtime().tm_year),month=4, day=30)

        #limite de 1 de maio ate 31 de Maio
        dtLim3=date(year=int(localtime().tm_year),month=5, day=1)
        dtLim4=date(year=int(localtime().tm_year),month=5, day=31)

        #limite de 1 de junho ate 30 de junho
        dtLim5=date(year=int(localtime().tm_year),month=6, day=1)
        dtLim6=date(year=int(localtime().tm_year),month=6, day=30)

        #limite de 1 de julho ate 31 de julho
        dtLim7=date(year=int(localtime().tm_year),month=7, day=1)
        dtLim8=date(year=int(localtime().tm_year),month=7, day=31)

        #limite de 1 de Agosto ate 31 de Agosto
        dtLim9=date(year=int(localtime().tm_year),month=8, day=1)
        dtLim10=date(year=int(localtime().tm_year),month=8, day=31)

        #limite de 1 de Setembro ate 31 de Dezembro
        dtLim11=date(year=int(localtime().tm_year),month=9, day=1)
        dtLim12=date(year=int(localtime().tm_year),month=12, day=31)

        if actual>=dtLim1 and actual<=dtLim2:
            serializado_s.update({'valor': 250})
        elif actual>=dtLim3 and actual<=dtLim4:
            serializado_s.update({'valor': 500})
        elif actual>=dtLim5 and actual<=dtLim6:
            serializado_s.update({'valor': 750})
        elif actual>=dtLim7 and actual<=dtLim8:
            serializado_s.update({'valor': 1000})
        elif actual>=dtLim9 and actual<=dtLim10:
            serializado_s.update({'valor': 1250})
        elif actual>=dtLim11 and actual<=dtLim12:
            serializado_s.update({'valor': 1500})

    return serializado_s['valor']