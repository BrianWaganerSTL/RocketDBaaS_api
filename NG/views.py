from django.shortcuts import render,  get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    DjangoModelPermissions,
    DjangoModelPermissionsOrAnonReadOnly
)
from django.http.response import HttpResponseNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import *
from .serializers import PoolServerSerializer

def poolServer(request):
    poolServer = PoolServer.objects.all()

    return render(request, 'poolServer.html', {'poolServer':poolServer})

def environments(request):
    environments = Environment.objects.all()
    return render(request, 'env.html', {'environment':environments})
from django.shortcuts import render

class PoolServerViewSet(viewsets.ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = PoolServerSerializer
    search_fields =('serverName','serverIp','dbms','cpu')
    ordering_fields = '__all__'
    ordering = ('-created_dttm',)
    lookup_field = ('serverName')
    permission_classes = [ ]

# class PoolServer(Model):
#     serverName = CharField(max_length=30, null=False)
#     serverIp = CharField(max_length=14, null=False)
#     dbms = CharField(choices=DBMS_TYPES, max_length=10, null=False)
#     cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
#     memGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
#     dbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
#     dataCenter = CharField(max_length=20, null=False)
#     activeSw = BooleanField(null=False)
#     createdDttm = DateTimeField(editable=False, auto_now_add=True)
#     updatedDttm = DateTimeField(auto_now=True)
