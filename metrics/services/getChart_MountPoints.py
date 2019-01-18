from django.http import HttpResponse
from django.utils import timezone
from rest_framework import authentication, status
from rest_framework.permissions import AllowAny
from rest_framework.utils import json
from rest_framework.views import APIView

from metrics.models import Metrics_MountPoint


class ChartMountPoints(APIView):
  authentication_classes = (authentication.TokenAuthentication,)
  permission_classes = [AllowAny, ]

  def get(self, request, vServerId):
    print('vServerId=' + str(vServerId))
    afterDttm = timezone.now() - timezone.timedelta(days=60)

    mountPoints = Metrics_MountPoint.objects \
      .filter(server_id=vServerId) \
      .filter(created_dttm__gte=afterDttm) \
      .exclude(mount_point='') \
      .order_by('-created_dttm')

    dataList = []
    mntSlashList = []
    mntDataList = []
    mntLogsList = []
    mntBkupsList = []
    mntHomeList = []
    mntTmpList = []
    mntCList = []


    for a in mountPoints:
      myDateStr = a.created_dttm.strftime("%Y-%m-%dT%H:%M:%S.000Z")
      dataPoint = {'name': myDateStr, 'value': str(a.used_pct) }

      if (a.mount_point == '/'):
        mntSlashList.append(dataPoint)
      elif (a.mount_point == '/opt/pgsql/data'):
        mntDataList.append(dataPoint)
      elif (a.mount_point == '/opt/pgsql/logs'):
        mntLogsList.append(dataPoint)
      elif (a.mount_point == '/opt/pgsql/backups'):
        mntBkupsList.append(dataPoint)
      elif (a.mount_point == '/home'):
        mntHomeList.append(dataPoint)
      elif (a.mount_point == '/tmp'):
        mntTmpList.append(dataPoint)
      elif (a.mount_point == 'C'):
        mntCList.append(dataPoint)
      else:
        continue

    dataList.append({'name': '/', 'series': mntSlashList })
    dataList.append({'name': 'data', 'series': mntDataList})
    dataList.append({'name': 'logs', 'series': mntLogsList})
    dataList.append({'name': 'backups', 'series': mntBkupsList})
    dataList.append({'name': 'home', 'series': mntHomeList})
    dataList.append({'name': 'tmp', 'series': mntTmpList})
    dataList.append({'name': 'C', 'series': mntCList})

    mountPointGraphData = json.dumps(dataList)

    return HttpResponse(mountPointGraphData, status=status.HTTP_200_OK)
