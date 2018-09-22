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
from .models import PoolServer, DbmsTypeChoices
from .serializers import *
from django.views.generic.base import ContextMixin
from django.views.generic import ListView
from django.http import HttpResponse
# def poolServer(request, dbms_type):
#     poolServer = PoolServer.objects.filter(dbmsType__exact=PoolServer.dbms_type)
#     return render(request, 'poolServer.html', {'poolServer':poolServer})
from django.shortcuts import render


def profile(request, NeededServers=3):
   return HttpResponse('<h1>hi username: {}</h1>'.format(NeededServers))


# .filter(statusInPool__exact=PoolServer.StatusInPoolChoices.Available) \
# .filter(dbmsType__iexact=PoolServer.dbms_type) \



    # def get_object(self):
    #     return get_object_or_404(PoolServer,
    #                              NeededServers=self.kwargs['NeededServers'])


# filter(statusInPool__iexact=PoolServer.StatusInPoolChoices.Available)[:self.poolServers.


class LockPoolServersViewSet(viewsets.ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = LockPoolServersSerializer
    permission_classes = [AllowAny,]
    # lookup_field = ('server_name')
#     queryset = PoolServer.objects.all()
#     search_fields =('server_name','server_ip','dbms_type','cpu')
#     ordering_fields = '__all__'
#     ordering = ('-created_dttm',)
#     permission_classes = [ ]

    # def __init__(self):

    # self.dbms_type = dbms_type
    #self.poolServersNeeded = poolServersNeeded

    # def get_queryset(self):
    #     print(self.request.query_params)
    #     print(self.lookup_url_kwarg)
    def poolserver_list(self,   poolServersNeeded):
        queryset = PoolServer.objects.filter(poolServersNeeded__=poolServersNeeded)
        # def detail(self, request, *args, **kwargs):
        # print("DbmsType="+dbms_type)
        #print(self.lookup_url_kwarg)
        poolServersQS = self.get_queryset()
        serializer = LockPoolServersSerializer(poolServersQS, many=True)

        #queryset = PoolServer.objects.filter(dbmsType__iexact=dbms_type).order_by('-created_dttm')
        #poolServers = request.filter_queryset(PoolServer.objects.filter(dbmsType__iexact=dbms_type))
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        print(self.request.query_params)
        print(self.lookup_url_kwarg)
        poolServersQS = self.get_queryset()
        serializer = LockPoolServersSerializer(poolServersQS, many=True)
        #queryset = PoolServer.objects.filter(dbmsType__iexact=dbms_type).order_by('-created_dttm')
        #poolServers = request.filter_queryset(PoolServer.objects.filter(dbmsType__iexact=dbms_type))
        return Response(serializer.data)
      # poolServers = self.request.query_params.items() #.get('status_in_pool', PoolServer.StatusInPoolChoices.AVAILABLE)
      # return poolServers

class MyPoolServersViewSet(viewsets.ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = MyPoolServersSerializer
