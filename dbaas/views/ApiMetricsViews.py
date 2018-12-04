from django.utils import timezone
from rest_framework import authentication, permissions, generics
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, )
from dbaas.models import MetricsCpu, MetricsPingServer, MetricsMountPoint, \
    MetricsLoad, MetricsPingDb
from dbaas.serializers.ApiMetricsSerializers import MetricsMountPointSerializer, MetricsLoadSerializer, MetricsCpuSerializer, \
    MetricsPingDbSerializer, MetricsPingServerSerializer

defaultMetricsMins = 60

class MetricsCpuList(generics.ListAPIView):
    queryset = MetricsCpu.objects.all()
    serializer_class = MetricsCpuSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return MetricsCpu.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class MetricsMountPointList(generics.ListAPIView):
    queryset = MetricsMountPoint.objects.all()
    serializer_class = MetricsMountPointSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(days=30)

        return MetricsMountPoint.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .exclude(mount_point='') \
            .order_by('-created_dttm')


class MetricsLoadList(generics.ListAPIView):
    queryset = MetricsLoad.objects.all()
    serializer_class = MetricsLoadSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return MetricsLoad.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class MetricsPingServerList(generics.ListAPIView):
    queryset = MetricsPingServer.objects.all()
    serializer_class = MetricsPingServerSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return MetricsPingServer.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class MetricsPingDbList(generics.ListAPIView):
    queryset = MetricsPingDb.objects.all()
    serializer_class = MetricsPingDbSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return MetricsPingDb.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')
