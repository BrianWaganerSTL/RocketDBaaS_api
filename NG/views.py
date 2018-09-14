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
    queryset = PoolServer.objects.filter(statusInPool__exact=PoolServer.StatusInPoolChoices.Available).order_by('createdDttm')
    serializer_class = PoolServerSerializer
    permission_classes = [AllowAny,]
#     queryset = PoolServer.objects.all()
#     serializer_class = PoolServerSerializer
#     search_fields =('serverName','serverIp','dbms','cpu')
#     ordering_fields = '__all__'
#     ordering = ('-created_dttm',)
#     lookup_field = ('serverName')
#     permission_classes = [ ]

    # def get_queryset(self):
      # poolServers = self.request.query_params.items() #.get('statusInPool', PoolServer.StatusInPoolChoices.AVAILABLE)
      # return poolServers
