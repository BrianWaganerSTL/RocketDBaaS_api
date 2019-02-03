from django.db.models import Q
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from monitor.models import ThresholdTest, Incident
from monitor.serializer import ThresholdTestSerializer, IncidentSerializer


class ThresholdTest(ModelViewSet):
    queryset = ThresholdTest.objects.all()
    serializer_class = ThresholdTestSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]


class IncidentList(generics.ListAPIView):
    serializer_class = IncidentSerializer
    permission_classes = [AllowAny, ]
    authentication_classes = [TokenAuthentication, ]
    lookup_field = 'vServerId'

    def get_queryset(self):
        vServerId = self.kwargs['vServerId']
        return Incident.objects.filter(server_id=vServerId).order_by('-last_dttm')

class IncidentAlertsViewSet(ModelViewSet):
  queryset = Incident.objects \
    .filter(Q(current_status=Incident.StatusChoices.WARNING) | Q(current_status=Incident.StatusChoices.CRITICAL)) \
    .order_by('-last_dttm')
  serializer_class = IncidentSerializer
  permission_classes = [AllowAny, ]
  authentication_classes = [TokenAuthentication, ]

