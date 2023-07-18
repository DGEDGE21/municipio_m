
from django.urls import path
from .views import payIpa,CheckIavPagamentoView, IavListView,payIav,CheckIpaPagamentoView, IpaListView, CheckPropPagamentoView, payProp, PropListView

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
    # Outras URLs do seu aplicativo...
]
