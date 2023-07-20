from django.urls import path
from .views import *

urlpatterns = [
    path('list/', TaxaListView.as_view(), name='taxa-list'),
    path('find/<str:rubrica>/', TaxaDetailView.as_view(), name='taxa-detail'),
    path('list-tae/', EstabelecimentoListAPIView.as_view(), name='tae-list'),
    # Outras URLs da sua aplicação...
]
