from rest_framework import serializers
from .models import *
from pagamentos.serializers import *

class LicensaAESerializer(serializers.ModelSerializer):
    pagamento=GenericoPagamentoSerializer()
    class Meta:
        model = LicensaAE
        fields = '__all__'


