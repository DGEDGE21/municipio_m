
from django.urls import path
from .views import *

urlpatterns = [
    path('pay-ipa/', payIpa.as_view(), name='pay-ipa'),
    path('check-ipa/', CheckIpaPagamentoView.as_view(), name='check-ipa-pagamento'),
    path('list-ipa/', IpaListView.as_view(), name='list-ipa-pagamento'),
    path('check-prop/', CheckPropPagamentoView.as_view(), name='check-prop-pagamento'),
    path('pay-prop/', payProp.as_view(), name='pay-prop'),
    path('list-prop/', PropListView.as_view(), name='list-prop-pagamento'),
    path('check-iav/', CheckIavPagamentoView.as_view(), name='check-iav-pagamento'),
    path('pay-iav/', payIav.as_view(), name='pay-iav'),
    path('list-iav/', IavListView.as_view(), name='list-iav-pagamento'),
    path('check-tae/', CheckTaePagamentoView.as_view(), name='check-tae-pagamento'),
    path('pay-tae/', payTae.as_view(), name='pay-tae'),
    path('list-tae/', TaeListView.as_view(), name='list-tae-pagamento'),
    path('pay-decl/', payDeclaracao.as_view(), name='pay-decl'),
    path('list-decl/', DeclaracaoListView.as_view(), name='list-decl'),
    path('check-decl/', DeclaracaoCheckView.as_view(), name='list-decl'),
    # Outras URLs do seu aplicativo...
]
