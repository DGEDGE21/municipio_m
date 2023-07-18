from django.urls import path
from .views import *
urlpatterns = [
    path('create/', PropriedadeCreateView.as_view(), name='municipe-create'),
    path('listByMunicipe/', PropriedadeListByMunicipeView.as_view(), name='propriedade-by-municipe'),
]
