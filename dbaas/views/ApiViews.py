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
from dbaas.serializers.ApiSerializers import ClusterSerializer, PoolServerSerializer, ServersSerializer, RestoresSerializer, BackupsSerializer, ServerActivitiesSerializer, \
    NotesSerializer, AlertsSerializer, ApplicationContactsSerializer
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

class PoolServerViewSet(ModelViewSet):
    queryset = PoolServer.objects.all()
    serializer_class = PoolServerSerializer
    permission_classes = [AllowAny, ]



