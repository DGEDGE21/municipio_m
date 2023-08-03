
from django.urls import path
from .views import *

urlpatterns = [
    # Outras URLs do seu aplicativo...
    path('create/', LicensaCreateView.as_view(), name='licensa'),
    path('aprovacao/', LicensaAprovarView.as_view(), name='licensa-aprovacao'),
    path('list/', LicensaListView.as_view(), name='licensa-list'),
    path('list-aproved/', LicensaAprovedView.as_view(), name='licensa-aprovacao-list'),
]
