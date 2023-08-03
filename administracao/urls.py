from django.urls import path
from .views import *

urlpatterns = [
    path('list-unidade/', UnidadeListAPIView.as_view(), name='unidade-list'),
    path('add/', FuncionarioCreateAPIView.as_view(), name='unidade-create'),
    path('list-users/', FuncionarioListAPIView.as_view(), name='funcionario-list'),
]