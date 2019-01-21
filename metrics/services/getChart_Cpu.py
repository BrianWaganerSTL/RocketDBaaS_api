from random import randint

from django.db.models.expressions import Random
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import authentication, status
from rest_framework.permissions import AllowAny
from rest_framework.utils import json
from rest_framework.views import APIView

from metrics.models import Metrics_MountPoint, Metrics_Cpu


class ChartCpus(APIView):
  authentication_classes = (authentication.TokenAuthentication,)
  permission_classes = [AllowAny, ]

  def get(self, request, vServerId):
    print('vServerId=' + str(vServerId))
    daysToDisplay = 60
    dataPoints = 720
    afterDttm = timezone.now() - timezone.timedelta(days=daysToDisplay)

    cpus = Metrics_Cpu.objects \
      .filter(server_id=vServerId) \
      .filter(created_dttm__gte=afterDttm) \
      .order_by('-created_dttm')

    dataList = []
    mntIdlePctList = []
    mntUserPctList = []
    mntSystemPctList = []
    mntIoWaitPctList = []
    mntStealPctList = []

    for a in cpus:
      myDateStr = a.created_dttm.strftime("%Y-%m-%dT%H:%M:%S.000Z")

      cpuIdlePct = int(a.cpu_idle_pct)
      cpuUserPct = int(a.cpu_user_pct)
      cpuSystemPct = int(a.cpu_system_pct)
      cpuIoWaitPct = int(a.cpu_iowait_pct)
      cpuStealPct = int(a.cpu_steal_pct)

      mntIdlePctList.append({'name': myDateStr, 'value': cpuIdlePct})
      mntUserPctList.append({'name': myDateStr, 'value': cpuUserPct})
      mntSystemPctList.append({'name': myDateStr, 'value': cpuSystemPct})
      mntIoWaitPctList.append({'name': myDateStr, 'value': cpuIoWaitPct})
      mntStealPctList.append({'name': myDateStr, 'value': cpuStealPct})

    # Reduce the number of plotpoint to be 300 or less
    for x in range(dataPoints, len(mntIdlePctList)):
      popIt = randint(0, len(mntIdlePctList)-1)
      mntIdlePctList.pop(popIt)
      mntUserPctList.pop(popIt)
      mntSystemPctList.pop(popIt)
      mntIoWaitPctList.pop(popIt)
      mntStealPctList.pop(popIt)

    dataList.append({'name': 'User', 'series': mntUserPctList})
    dataList.append({'name': 'System', 'series': mntSystemPctList})
    dataList.append({'name': 'IO Waits', 'series': mntIoWaitPctList})
    dataList.append({'name': 'Steal', 'series': mntStealPctList})
    dataList.append({'name': 'Idle', 'series': mntIdlePctList})
    # Idle list must be appended last to be on the TOP of the graph

    graphData = json.dumps(dataList)

    return HttpResponse(graphData, status=status.HTTP_200_OK)
