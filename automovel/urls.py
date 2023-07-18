from django.urls import path
from .views import *
urlpatterns = [
    path('create/', AutomovelCreateView.as_view(), name='municipe-create'),
    path('listByMunicipe/<int:id_municipe>/', AutomovelListByMunicipeView.as_view(), name='veiculos-by-municipe'),
    path('createGrupo/', AutomovelGrupoCreateView.as_view(), name='auto-grupo-create'),
    path('createEscalao/', AutomovelGrupoEscalaoCreateView.as_view(), name='auto-grupo-create'),
    
]
