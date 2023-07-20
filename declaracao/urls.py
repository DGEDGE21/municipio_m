from django.urls import path
from .views import *
urlpatterns = [
    path('create/', DeclaracaoCreateView.as_view(), name='declaracao-create'),
    
]
