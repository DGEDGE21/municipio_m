from django.urls import path
from .views import *
urlpatterns = [
    path('create/', EstabelecimentoCreateView.as_view(), name='estabelecimento-create'),
    path('listByMunicipe/', EstabelecimentoListByMunicipeView.as_view(), name='estabelecimento-by-municipe'),
]
