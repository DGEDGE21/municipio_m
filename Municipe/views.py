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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from django.shortcuts import render

class MunicipeCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MunicipeCreateSerializer

class BairroListView(ListAPIView):
    queryset = Bairro.objects.all()
    serializer_class = BairroSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class MunicipeListView(ListAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class MunicipeDetailView(RetrieveAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'nr_contribuente'
    lookup_url_kwarg = 'nr_contribuente'

class MunicipeUpdateView(UpdateAPIView):
    queryset = Municipe.objects.all()
    serializer_class = MunicipeUpdateSerializer
    lookup_field = 'id'  # Campo utilizado para a busca do objeto

    def get_serializer_context(self):
        # Inclui o request na contexto do serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


