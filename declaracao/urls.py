from django.urls import path
from .views import *
urlpatterns = [
    path('create/', DeclaracaoCreateView.as_view(), name='declaracao-create'),
    path('list/', DeclaracaoListView.as_view(), name='declaracao-list'),
    path('aprovacao/', DeclaracaoAprovarView.as_view(), name='declaracao-aprovacao'),
    path('list-aproved/', DeclaracaoAprovadaView.as_view(), name='declaracao-aprovacao-list'),
    path('novo-pedido/', NovoPedido.as_view(), name='declaracao-pedido'),
    path('list-pedido-municipe/<str:nr_contribuente>/', DeclaracaoMunicipeView.as_view(), name='declaracao-pedido-list'),
]
