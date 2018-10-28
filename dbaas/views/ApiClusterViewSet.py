from django.template import RequestContext
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser,)
from dbaas.models import PoolServer, Cluster, Server
from dbaas.serializers.CreateClusterSerializer import ClusterSerializer, ServerSerializer, PoolServerSerializer
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

class ClusterViewSet(ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [AllowAny,]
    authentication_classes = [TokenAuthentication,]

    #lookup_field = 'cluster_name'

    # @action(detail=False)
    # def list_clusters(self, request, pk=None):
    #     cluster = self.get_object()
    #     return Response(cluster)
    #
    # @action(detail=True)
    # def cluster_details(self, request, pk=None):
    #     cluster = self.get_object()
    #     servers = cluster.server_set()
    #     return Response([server.server_name for server in servers])

class ServerViewSet(ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


class PoolServerViewSet(ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = PoolServerSerializer




