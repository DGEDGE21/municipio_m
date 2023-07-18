from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from time import *
from datetime import *
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import SessionAuthentication
from knox.auth import TokenAuthentication
from time import *
from django.db.models import Q
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db import transaction
from tablib import Dataset
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from unidecode import unidecode
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        try:
            serializer = AuthTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            grupo = None
            identifica = None
            if user.groups.exists():
                grupo = user.groups.all()[0].name
                identifica = user.username
            _, token = AuthToken.objects.create(user=user)

            return Response(data={'token': token,  'grupo': grupo,  'username': identifica, 'status': 200}, status=200)
        except AuthenticationFailed as e:
            return Response(data={'message': str(e)}, status=401)
        except Exception as e:
            return Response(data={'message': 'Erro no login'}, status=500)
        

