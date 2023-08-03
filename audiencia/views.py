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