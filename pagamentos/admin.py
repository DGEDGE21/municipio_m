from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Pagamento)
admin.site.register(IpaPagamento)
admin.site.register(PropPagamento)
admin.site.register(IavPagamento)
admin.site.register(DeclaracaoPagamento)
admin.site.register(UrbPagamento)
admin.site.register(PubPagamento)
admin.site.register(TransPagamento)
admin.site.register(ResidualPagamento)