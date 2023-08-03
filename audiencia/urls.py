from django.urls import path
from .views import *

urlpatterns = [
    path('create/', AudienciaCreateView.as_view(), name='audiencia-create'),
    path('list/', AudienciaListarView.as_view(), name='audiencia-list'),
]