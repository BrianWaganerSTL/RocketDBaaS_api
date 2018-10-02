from django.template import RequestContext
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser,)
from ng.models2 import PoolServer, Cluster, Server
from ng.serializers.CreateClusterSerializer import ClusterSerializer, ServerSerializer, PoolServerSerializer
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response


class ClusterViewSet(ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = Cluster.objects.all()
    permission_classes = [AllowAny,]

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




