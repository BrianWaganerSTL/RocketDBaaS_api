import order as order
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
from dbaas.models import PoolServer, Cluster, Server, Backup, Restore, ServerActivity, ClusterNote, Alert, ApplicationContact
from dbaas.serializers.ApiSerializers import ClusterSerializer, ServersSerializer, RestoresSerializer, BackupsSerializer, ServerActivitiesSerializer, \
    NotesSerializer, AlertsSerializer, ApplicationContactsSerializer, PoolServersSerializer
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

# TODO: Need to refactor since with this committed out I can't do partial name searches from the UI
    # def get_queryset(self):
    #     clusters = Cluster.objects.all()
    #     queryClusterName = self.request.GET.get('cluster_name')
    #     if queryClusterName is not None:
    #         clusters = clusters.filter(cluster_name__icontains=queryClusterName)
    #     return clusters

class BackupsList(generics.ListAPIView):
    serializer_class = BackupsSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vClusterId'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return Backup.objects.filter(cluster_id=vClusterId).order_by('-start_dttm')

class RestoresList(generics.ListAPIView):
    serializer_class = RestoresSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vClusterId'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return Restore.objects.filter(to_cluster_id=vClusterId).order_by('-start_dttm')

class ActivitiesList(generics.ListAPIView):
    serializer_class = ServerActivitiesSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vClusterId'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return ServerActivity.objects.filter(server__cluster_id=vClusterId).order_by('-start_dttm')

class NotesList(generics.ListAPIView):
    serializer_class = NotesSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vClusterId'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return ClusterNote.objects.filter(cluster_id=vClusterId).order_by('-created_dttm')

class AlertsList(generics.ListAPIView):
    serializer_class = AlertsSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vClusterId'

    def get_queryset(self):
        vClusterId = self.kwargs['vClusterId']
        return Alert.objects.filter(cluster_id=vClusterId).order_by('-created_dttm')

class ApplicationContactsList(generics.ListAPIView):
    serializer_class = ApplicationContactsSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vApplicationId'

    def get_queryset(self):
        vApplicationId = self.kwargs['vApplicationId']
        return ApplicationContact.objects.filter(application__exact=vApplicationId).filter(active_sw=True)

# class PoolServerList(ModelViewSet):
#     # queryset = PoolServer.objects.filter(status_in_pool__in={'Available', 'Locked'})
#     queryset = PoolServer.objects
#     serializer_class = PoolServerSerializer
#     permission_classes = [AllowAny, ]
#     authentication_classes = [TokenAuthentication, ]

class PoolServersViewSet(ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = PoolServersSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        queryset = PoolServer.objects.all().order_by('environment','data_center','dbms_type','-created_dttm')

        env = self.request.query_params.get('env', None)
        if env is not None:
            queryset = queryset.filter(environment__iexact = env)

        dbms = self.request.query_params.get('dbms', None)
        if dbms is not None:
            queryset = queryset.filter(dbms_type__iexact = dbms)

        req_cpu = self.request.query_params.get('req_cpu', None)
        if req_cpu is not None:
            queryset = queryset.filter(cpu__gte = req_cpu)

        req_mem_gb = self.request.query_params.get('req_mem_gb', None)
        if req_mem_gb is not None:
            queryset = queryset.filter(mem_gb__gte = req_mem_gb)

        req_db_gb = self.request.query_params.get('req_db_gb', None)
        if req_db_gb is not None:
            queryset = queryset.filter(db_gb__gte = req_db_gb)

        statusInPool = self.request.query_params.get('status_in_pool', None)
        if statusInPool is not None:
            queryset = queryset.filter(status_in_pool__iexact = statusInPool)

        return queryset