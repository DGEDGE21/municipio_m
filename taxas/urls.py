from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TaxaListView.as_view(), name='taxa-list'),
    path('find/<str:rubrica>/', TaxaDetailView.as_view(), name='taxa-detail'),
    path('list-tae/', EstabelecimentoListAPIView.as_view(), name='tae-list'),
    path('calculoUrbanizacao/', calculo_urbanizacao.as_view(), name='tae-list'),
    path('calculoPublicidade/', calculo_publicidade.as_view(), name='tae-list'),
    path('cadastrar/', cadastrar_taxas.as_view(), name='tae-list'),
    # Outras URLs da sua aplicação...
]
