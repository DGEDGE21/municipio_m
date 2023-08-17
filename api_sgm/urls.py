"""api_sgm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
admin.site.site_header='SGM ADMIN'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include('central.urls')),
    path("municipe/",include('Municipe.urls')),
    path("automovel/",include('automovel.urls')),
    path("propriedade/",include('Propriedade.urls')),
    path("impostos/",include('impostos.urls')),
    path("taxas/",include('taxas.urls')),
    path("bills/",include('pagamentos.urls')),
    path("estabelecimento/",include('estabelecimento.urls')),
    path("declaracao/",include('declaracao.urls')),
    path("urbanizacao/",include('urbanizacao.urls')),
    path("administracao/",include('administracao.urls')),
    path("audiencia/",include('audiencia.urls')),
    path("planificacao/",include('planificacao.urls')),
]
