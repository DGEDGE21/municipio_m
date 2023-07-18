from django.urls import path
from .views import *

urlpatterns = [
    path('list/', ImpostoListView.as_view(), name='imposto-list'),
    path('find/<str:rubrica>/', ImpostoDetailView.as_view(), name='imposto-detail'),
    path('list-ipa/', MunicipeListAPIView.as_view(), name='ipa-list'),
    path('list-prop/', PropriedadeListAPIView.as_view(), name='prop-list'),
    path('list-iav/', AutomovelListAPIView.as_view(), name='iav-list'),
    # Outras URLs da sua aplicação...
]
