from rest_framework import serializers
from .models import *
from pagamentos.serializers import *

class LicensaTransporteSerializer(serializers.ModelSerializer):
    pagamento=UrbPagamentoSerializer()
    veiculo=AutomovelSerializer()
    class Meta:
        model = LicensaTransporte
        fields = '__all__'

class LicensaAguaSerializer(serializers.ModelSerializer):
    pagamento=UrbPagamentoSerializer()
    class Meta:
        model = LicensaAgua
        fields = '__all__'

