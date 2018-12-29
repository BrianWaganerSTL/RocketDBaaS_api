from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import (AllowAny, )

from metrics.models import Metrics_Cpu, Metrics_MountPoint, Metrics_CpuLoad, Metrics_PingServer, Metrics_PingDb
from metrics.serializers import Metrics_MountPointSerializer, Metrics_CpuLoadSerializer, Metrics_CpuSerializer, Metrics_PingServerSerializer, Metrics_PingDbSerializer

defaultMetricsMins = 180

class Metrics_CpuList(generics.ListAPIView):
    queryset = Metrics_Cpu.objects.all()
    serializer_class = Metrics_CpuSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return Metrics_Cpu.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class Metrics_MountPointList(generics.ListAPIView):
    queryset = Metrics_MountPoint.objects.all()
    serializer_class = Metrics_MountPointSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(days=30)

        return Metrics_MountPoint.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .exclude(mount_point='') \
            .order_by('-created_dttm')


class Metrics_CpuLoadList(generics.ListAPIView):
    queryset = Metrics_CpuLoad.objects.all()
    serializer_class = Metrics_CpuLoadSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return Metrics_CpuLoad.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class Metrics_PingServerList(generics.ListAPIView):
    queryset = Metrics_PingServer.objects.all()
    serializer_class = Metrics_PingServerSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return Metrics_PingServer.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class Metrics_PingDbList(generics.ListAPIView):
    queryset = Metrics_PingDb.objects.all()
    serializer_class = Metrics_PingDbSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return Metrics_PingDb.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')
