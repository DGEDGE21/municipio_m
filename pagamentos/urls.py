
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
    path('pay-urb/', payUrb.as_view(), name='pay-urb'),
    path('list-urb/', UrbListView.as_view(), name='list-urb'),
    path('pay-pub/', payPub.as_view(), name='pay-urb'),
    path('list-pub/', PubListView.as_view(), name='list-urb'),
    path('pay-trans/', payTrans.as_view(), name='pay-trans'),
    path('list-trans/', TransListView.as_view(), name='list-trans'),
    path('list-impostos/', ListImpostos.as_view(), name='list-impostos'),
    path('list-taxas/', ListTaxas.as_view(), name='list-taxas'),
    path('check-urb/', UrbanizacaoCheckView.as_view(), name='check-urb'),
    path('pay-residual/', payResidual.as_view(), name='pay-residual'),
    path('list-residual/', ResidualListView.as_view(), name='list-residual'),
    path('pay-mercado/', payMercado.as_view(), name='pay-mercado'),
    path('list-mercado/', MercadoListView.as_view(), name='list-mercado'),
    path('pay-generico/', payGenerico.as_view(), name='pay-generico'),
    path('list-generico/', GenericoListView.as_view(), name='list-generico'),
     path('municipe-pagamentos/<str:nr_contribuinte>/', MunicipePagamentos.as_view(), name='municipe-pagamentos'),
    # Outras URLs do seu aplicativo...
]
