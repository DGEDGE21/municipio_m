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
from taxas.models import *
from rest_framework import status

class AudienciaCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        try:
            user = request.user
            usuario = User.objects.get(username=user)

            municipe = Municipe.objects.get(
                nr_contribuente=self.request.data['nr_contribuente']
            )
            audiencia = Audiencia.objects.create(
                municipe=municipe,
                descricao=self.request.data['descricao'],
                data=self.request.data['data'],
                hora=self.request.data['hora'],
                local=self.request.data['local'],
                estado='Marcado',
                user=usuario
            )
            audiencia.save()
            audiencia_serializer = AudienciaSerializer(audiencia).data
            return Response(audiencia_serializer, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'detail': 'Erro ao criar audiencia'}, status=status.HTTP_400_BAD_REQUEST)

#lista as audiencias com status marcado
class AudienciaListarView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AudienciaSerializer
    def get_queryset(self):
        return Audiencia.objects.filter(estado='Marcado')

#faz uma view para mudar o estado da audiencia para cancelado
class AudienciaCancelarView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            audiencia = Audiencia.objects.get(id=self.kwargs['pk'])
            audiencia.estado = 'Cancelado'
            audiencia.save()
            return Response({'detail': 'Audiencia cancelada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'Erro ao cancelar audiencia'}, status=status.HTTP_400_BAD_REQUEST)

#faz uma view para mudar o estado da audiencia para realizado
class AudienciaRealizadoView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            audiencia = Audiencia.objects.get(id=self.kwargs['pk'])
            audiencia.estado = 'Realizado'
            audiencia.save()
            return Response({'detail': 'Audiencia realizada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'Erro ao realizar audiencia'}, status=status.HTTP_400_BAD_REQUEST)

#lista as audiencias com status diferente de marcado e Em espera
class AudienciaListarRealizadasView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AudienciaSerializer
    def get_queryset(self):
        return Audiencia.objects.exclude(estado='Marcado').exclude(estado='Em espera')

#lista as audiencias com status Em espera
class AudienciaListarEmEsperaView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AudienciaSerializer
    def get_queryset(self):
        return Audiencia.objects.filter(estado='Em espera')
#lista as audiencias de um municipe
class AudienciaListarMunicipeView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AudienciaSerializer
    def get_queryset(self, *args, **kwargs):
        return Audiencia.objects.filter(municipe__nr_contribuente=self.kwargs['nr_contribuente'])

#faz uma view que pega uma audiencia pelo seu pk e faz update de data, hora e local
class AudienciaUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        try:
            audiencia = Audiencia.objects.get(id=self.kwargs['pk'])
            audiencia.data = self.request.data['date']
            audiencia.hora = self.request.data['time']
            audiencia.local = self.request.data['place']
            audiencia.estado = "Marcado"
            audiencia.save()
            return Response({'detail': 'Audiencia alterada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'detail': 'Erro ao alterar audiencia'}, status=status.HTTP_400_BAD_REQUEST)

class PedidoAudiencia(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        try:
            user = request.user
            usuario = User.objects.get(username=user)

            municipe = Municipe.objects.get(
                nr_contribuente=self.request.data['nca']
            )
            audiencia = Audiencia.objects.create(
                municipe=municipe,
                descricao='PEDIDO DE AUDIENCIA',
                estado='Em espera',
                pedido=self.request.data['minuta'],
            )
            audiencia.save()
            audiencia_serializer = AudienciaSerializer(audiencia).data
            return Response(audiencia_serializer, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'detail': 'Erro ao criar audiencia'}, status=status.HTTP_400_BAD_REQUEST)
