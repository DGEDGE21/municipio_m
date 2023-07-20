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
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.shortcuts import render
from django.db.models import Q

class EstabelecimentoCreateView(CreateAPIView):
    serializer_class = EstabelecimentoCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



class EstabelecimentoListByMunicipeView(ListAPIView):
    serializer_class = EstabelecimentoSerializer

    def get_queryset(self):
        search_term = self.request.query_params.get('search')  # Obtém o termo de pesquisa da URL

        queryset = Estabelecimento.objects.all()

        if search_term:
            queryset = queryset.filter(
                Q(id_municipe=search_term) | Q(id_municipe__nr_contribuente=search_term)
            )

        return queryset
