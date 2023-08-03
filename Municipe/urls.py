from django.urls import path
from .views import BairroListView, MunicipeListView,MunicipeUpdateView, MunicipeDetailView, MunicipeCreateView, MunicipePagamentosView

urlpatterns = [
    path('create/', MunicipeCreateView.as_view(), name='municipe-create'),
    path('bairros/', BairroListView.as_view(), name='bairro-list'),
    path('list/', MunicipeListView.as_view(), name='municipe-list'),
    path('update/<int:id>/', MunicipeUpdateView.as_view(), name='municipe-update'),
    path('find/<str:nr_contribuente>/', MunicipeDetailView.as_view(), name='municipe-detail'),
    path('pagamentos/<str:nr_contribuinte>/', MunicipePagamentosView.as_view(), name='municipe-pagamentos'),
]
