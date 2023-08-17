from rest_framework import serializers
from .models import *
from pagamentos.serializers import *

class LicensaTransporteSerializer(serializers.ModelSerializer):
    pagamento=TransPagamentoSerializer()
    veiculo=AutomovelSerializer()
    class Meta:
        model = LicensaTransporte
        fields = '__all__'

class LicensaAguaSerializer(serializers.ModelSerializer):
    pagamento=TransPagamentoSerializer()
    class Meta:
        model = LicensaAgua
        fields = '__all__'

