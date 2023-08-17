from rest_framework import generics, permissions
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from administracao.serializers import *
from Municipe.models import *
from Municipe.serializers import *
class LoginAPI2(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            grupo = None
            identifica = None
            if user.groups.exists():
                grupo = user.groups.all()[0].name
                identifica = user.username
            _, token = AuthToken.objects.create(user=user)

            prof=Municipe.objects.get(user=user)
            prof_s = MunicipeSerializer(prof).data
            #pega o username e faz slice para pegar o conteudo antes do @
            username = user.username.split('@')[0]
            nome=prof.nome

            return Response(data={'token': token,'username': username, 'nome':nome, 'nca':prof.nr_contribuente,'status': 200}, status=200)
        except AuthenticationFailed as e:
            return Response(data={'message': str(e)}, status=401)
        except Exception as e:
            return Response(data={'message': 'Erro no login'}, status=500)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            grupo = None
            identifica = None
            if user.groups.exists():
                grupo = user.groups.all()[0].name
                identifica = user.username
            _, token = AuthToken.objects.create(user=user)

            prof=Funcionario.objects.get(user=user)
            prof_s = FuncionarioSerializer(prof).data
            #pega o username e faz slice para pegar o conteudo antes do @
            username = user.username.split('@')[0]
            nome=prof.municipe.nome
            #pega o nome do funcionario
            unidade = prof.unidade.nome
            unidade_id=prof.unidade.id

            return Response(data={'token': token,  'grupo': grupo,  'unidade':unidade,'id_unidade':unidade_id,'username': username, 'nome':nome,'status': 200}, status=200)
        except AuthenticationFailed as e:
            return Response(data={'message': str(e)}, status=401)
        except Exception as e:
            return Response(data={'message': 'Erro no login'}, status=500)
        

