from django.urls import path
from .views import *

urlpatterns = [
    path('create/', AudienciaCreateView.as_view(), name='audiencia-create'),
    path('list/', AudienciaListarView.as_view(), name='audiencia-list'),
    path('cancelar/<int:pk>/', AudienciaCancelarView.as_view(), name='audiencia-cancelar'),
    path('realizado/<int:pk>/', AudienciaRealizadoView.as_view(), name='audiencia-realizado'),
    path('historico/', AudienciaListarRealizadasView.as_view(), name='audiencia-listar-realizados'),
    path('pedidos/', AudienciaListarEmEsperaView.as_view(), name='audiencia-pedido-municipe'),
    path('aceitar/<int:pk>/', AudienciaUpdateView.as_view(), name='audiencia-aceitar'),
    path('municipe_list/<str:nr_contribuente>/', AudienciaListarMunicipeView.as_view(), name='audiencia-list-municipe'),
    path('novo-pedido/', PedidoAudiencia.as_view(), name='audiencia-recusar'),

]