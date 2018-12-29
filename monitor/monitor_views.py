from django.shortcuts import render
from django.utils import timezone
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from metrics.metrics_views import defaultMetricsMins
from monitor.models import ThresholdTest, Incident
from monitor.serializer import ThresholdTestSerializer, IncidentSerializer


class ThresholdTestList(generics.ListAPIView):
    queryset = ThresholdTest.objects.all()
    serializer_class = ThresholdTestSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)

        return ThresholdTest.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .order_by('-created_dttm')


class IncidentList(generics.ListAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vServerId'

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        return Incident.objects.filter(server_id=vServerId).order_by('-created_dttm')