from django.core.serializers import json
from django.db.models.functions import Replace
from django.http import HttpResponse
from django.utils import timezone
from psycopg2._json import Json
from rest_framework import authentication, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from metrics.metrics_views import defaultMetricsMins
from metrics.models import Metrics_CpuLoad, Metrics_MountPoint


class ChartMountPoints(APIView):
  authentication_classes = (authentication.TokenAuthentication,)
  permission_classes = [AllowAny, ]

  defaultMetricsMins = 180

  def get(self, request, vServerId):
    print('vServerId=' + str(vServerId))

    # afterDttm = timezone.now() - timezone.timedelta(minutes=defaultMetricsMins)
    afterDttm = timezone.now() - timezone.timedelta(days=30)

    mountPoints = Metrics_MountPoint.objects \
            .filter(server_id=vServerId) \
            .filter(created_dttm__gte=afterDttm) \
            .exclude(mount_point='') \
            .order_by('-created_dttm')

    mntSlashDP = ''
    mntDataDP = ''
    mntLogsDP = ''
    mntBkupsDP = ''
    mntHomeDP = ''
    mntTmpDP = ''

    for a in mountPoints:
      myDateStr = a.created_dttm.strftime("%Y-%m-%d %H:%M")
      element = "{'name': new Date('" + myDateStr + "'), 'value': " + str(a.used_pct) + "}"

      if (a.mount_point == '/'):
        mntSlashDP += element
      elif (a.mount_point == '/opt/pgsql/data'):
        mntDataDP += element
      elif (a.mount_point == '/opt/pgsql/logs'):
        mntLogsDP += element
      elif (a.mount_point == '/opt/pgsql/backups'):
        mntBkupsDP += element
      elif (a.mount_point == '/home'):
        mntHomeDP += element
      elif (a.mount_point == '/tmp'):
        mntTmpDP += element
      else:
        continue

    mountPointGraphData = [
      {"name": '/', "series": mntSlashDP.replace("'","\"")},
      {"name": 'data', "series": mntDataDP.replace("'","\"")},
      {"name": 'logs', "series": mntLogsDP.replace("'","\"")},
      {"name": 'backups', "series": mntBkupsDP.replace("'","\"")},
      {"name": 'home', "series": mntHomeDP.replace("'","\"")},
      {"name": 'tmp', "series": mntTmpDP.replace("'","\"")},
    ];

    return HttpResponse(mountPointGraphData, status=status.HTTP_200_OK)
