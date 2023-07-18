from django.urls import path,include
from knox import views as knox_views
from .views import *


urlpatterns = [
    path('signin/', LoginAPI.as_view(), name='login'),
]