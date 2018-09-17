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
from django.http import  request
from django.http.response import HttpResponseNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import PoolServer, Environment
from .serializers import LockPoolServersSerializer

# def poolServer(request, dbmsType):
#     poolServer = PoolServer.objects.filter(dbmsType__exact=PoolServer.dbmsType)
#     return render(request, 'poolServer.html', {'poolServer':poolServer})

def environments(request):
    environments = Environment.objects.all()
    return render(request, 'environment.html', {'environment':environments})
from django.shortcuts import render


# .filter(statusInPool__exact=PoolServer.StatusInPoolChoices.Available) \
# .filter(dbmsType__iexact=PoolServer.dbmsType) \

class LockPoolServersViewSet(viewsets.ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = LockPoolServersSerializer
    permission_classes = [AllowAny,]
    lookup_field = ('serverName')
#     queryset = PoolServer.objects.all()
#     search_fields =('serverName','serverIp','dbmsType','cpu')
#     ordering_fields = '__all__'
#     ordering = ('-created_dttm',)
#     permission_classes = [ ]

    # def __init__(self):

    # self.dbmsType = dbmsType
    #self.poolServersNeeded = poolServersNeeded

    # def get_queryset(self):
    #     print(self.request.query_params)
    #     print(self.lookup_url_kwarg)
    def poolserver_list(self,   poolServersNeeded):
        queryset = PoolServer.objects.filter(poolServersNeeded__=poolServersNeeded)
        # def detail(self, request, *args, **kwargs):
        # print("DbmsType="+dbmsType)
        #print(self.lookup_url_kwarg)
        poolServersQS = self.get_queryset()
        serializer = PoolServerSerializer(poolServersQS, many=True)
        #queryset = PoolServer.objects.filter(dbmsType__iexact=dbmsType).order_by('-createdDttm')
        #poolServers = request.filter_queryset(PoolServer.objects.filter(dbmsType__iexact=dbmsType))
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        print(self.request.query_params)
        print(self.lookup_url_kwarg)
        poolServersQS = self.get_queryset()
        serializer = PoolServerSerializer(poolServersQS, many=True)
        #queryset = PoolServer.objects.filter(dbmsType__iexact=dbmsType).order_by('-createdDttm')
        #poolServers = request.filter_queryset(PoolServer.objects.filter(dbmsType__iexact=dbmsType))
        return Response(serializer.data)
      # poolServers = self.request.query_params.items() #.get('statusInPool', PoolServer.StatusInPoolChoices.AVAILABLE)
      # return poolServers
