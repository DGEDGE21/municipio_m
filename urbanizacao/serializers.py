from rest_framework import serializers
from .models import *
from pagamentos.serializers import *

class LicensaSerializer(serializers.ModelSerializer):
    pagamento=UrbPagamentoSerializer()
    class Meta:
        model = LicensaBase
        fields = '__all__'


class LicensaDuatSerializer(serializers.ModelSerializer):
    pagamento=UrbPagamentoSerializer()
    class Meta:
        model = LicensaDuat
        fields = '__all__'

class LicensaConstrucaoSerializer(serializers.ModelSerializer):
    pagamento=UrbPagamentoSerializer()
    class Meta:
        model = LicensaConstrucao
        fields = '__all__'