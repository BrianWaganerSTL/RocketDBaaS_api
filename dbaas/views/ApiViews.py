
from django.template import RequestContext
from django_filters import rest_framework
from django_filters.rest_framework import filters
from rest_framework import authentication, permissions, generics
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser,)
from dbaas.models import PoolServer, Cluster, Server
from dbaas.serializers.ApiSerializers import ClusterSerializer, PoolServerSerializer, ServersSerializer
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


class ServersList(generics.ListAPIView):
    serializer_class = ServersSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = '_cluster_id'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return Server.objects.filter(active_sw=True).filter(cluster_id=vClusterId)


class Clusters(ModelViewSet):
    queryset = Cluster.objects.all()
    serializer_class = ClusterSerializer
    permission_classes = [AllowAny,]
    authentication_classes = [TokenAuthentication,]
    lookup_field = 'cluster_name'

    def get_queryset(self):
        clusters = Cluster.objects.all()
        queryClusterName = self.request.GET.get('cluster_name')
        if queryClusterName is not None:
            clusters = clusters.filter(cluster_name__icontains=queryClusterName)
        return clusters


# class ClusterServers(ModelViewSet):
#     queryset = Server.objects.all()
#     serializer_class = ClusterServersSerializer
#     permission_classes = [AllowAny, ]
#     authentication_classes = [TokenAuthentication, ]
#     lookup_url_kwarg = "clusterId" # search item name in url
#     lookup_field = "cluster"       # search item name in model

    # def get_queryset(self):
    #     queryClusterId = self.kwargs['clusterId']
    #     # queryClusterId = self.request.query_params.get('clusterId', None)
    #     if queryClusterId is not None:
    #         queryset = self.queryset.filter(cluster_id=queryClusterId)
    #     return queryset


# def ClusterServers(request):
#     queryClusterId = request.content_params.get('clusterId')
#     servers = Server.objects.filter(active_sw=True).filter(cluster_id=queryClusterId)
#     return { 'servers': servers }
# class ClusterServersView(APIView):
#     authentication_classes = [TokenAuthentication, ]
#     permission_classes = [AllowAny, ]
#     renderer_classes = (JSONRenderer,)
#
#     def get(self, request, _cluster_id):
#         queryset = Server.objects.\
#             filter(active_sw=True).\
#             filter(cluster_id=_cluster_id)
#
#         serializer_class = ClusterServersSerializer(data=queryset)
#         print('serializer:' + serializer_class.initial_data)
#
#         return Response({'servers': serializer_class.data})

class PoolServerViewSet(ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = PoolServerSerializer
    permission_classes = [AllowAny, ]



