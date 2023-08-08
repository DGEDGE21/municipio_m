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
from django.db import transaction
from .permissions import *
from django.contrib.auth.hashers import make_password

#me faca view para retornar todas unidades
class UnidadeListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Unidade.objects.all()
    serializer_class = UnidadeSerializer

#me faca view para retornar todos funcionarios
class FuncionarioListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

#me faca view para criar um funcionario
class FuncionarioCreateAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        print(self.request.data)
        unidade=Unidade.objects.get(nome=self.request.data['unidade'])
        municipe=Municipe.objects.get(nr_contribuente=self.request.data['nr_contribuente'])
        print(1)
        lastName=municipe.nome.split()[-1]
        firstName=municipe.nome.split()[0]
        username = firstName.lower()+'.'+lastName.lower()+str(municipe.id)+'@sgm.gov.mz'
        print(2)
        #criar o user
        default_password='sgm@2023'
        serializer = self.get_serializer(data={"username": f"{username}", "password": make_password(default_password),
            "first_name": f"{firstName}", "last_name": f"{lastName}"})
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        print(3)
        try:
            #pegar o grupo
            gg = Group.objects.get(name=self.request.data['acesso'])
            usuario.groups.add(gg)
        except:
            pass
        usuario = serializer.save()

        funcionario=Funcionario.objects.create(
            municipe=municipe,
            unidade=unidade,
            user=usuario,
            cargo=self.request.data['acesso'],
        )
        func = FuncionarioSerializer(funcionario).data
        return Response(func, status=status.HTTP_201_CREATED)	
    