from random import randint

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import authentication, status
from rest_framework.permissions import AllowAny
from rest_framework.utils import json
from rest_framework.views import APIView

from metrics.models import Metrics_Cpu


class ChartCpus(APIView):
  authentication_classes = (authentication.TokenAuthentication,)
  permission_classes = [AllowAny, ]

  def get(self, request, vServerId):
    print('vServerId=' + str(vServerId))
    daysToDisplay = 2
    dataPoints = 500  # 1100 If you have too much data you tend to get   Error: <path> attribute d: Expected number, "…3.7967062844714,NaNL198.78843219…" MUST BE BAD DATA, or MEMORY
    afterDttm = timezone.now() - timezone.timedelta(days=daysToDisplay)

    cpus = Metrics_Cpu.objects \
      .filter(server_id=vServerId) \
      .filter(created_dttm__gte=afterDttm) \
      .filter(error_cnt=0) \
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

    for x in range(len(mntIdlePctList)-1, 0, -1):
      mntIdlePctList[x]['value'] = 100 - (mntUserPctList[x]['value'] + mntSystemPctList[x]['value'] + mntIoWaitPctList[x]['value'] + mntStealPctList[x]['value'])
      if ((mntIdlePctList[x]['value'] + (mntUserPctList[x]['value'] + mntSystemPctList[x]['value'] + mntIoWaitPctList[x]['value'] + mntStealPctList[x]['value'])) != 100):
        print(mntIdlePctList[x]['name'] + ' does not add up to 100%, but ' + str(mntIdlePctList[x]['value'] + mntUserPctList[x]['value'] + mntSystemPctList[x]['value'] + mntIoWaitPctList[x]['value'] + mntStealPctList[x]['value']))
      if (not (0 < mntIdlePctList[x]['value'] <= 100)):
        print(mntIdlePctList[x]['name'] + ' odd number ' + str(mntIdlePctList[x]['value']))
      if (not (0 <= mntUserPctList[x]['value'] <= 100)):
        print(mntUserPctList[x]['name'] + ' odd number ' + str(mntUserPctList[x]['value']))
      if (not (0 <= mntSystemPctList[x]['value'] <= 100)):
        print(mntSystemPctList[x]['name'] + ' odd number ' + str(mntSystemPctList[x]['value']))
      if (not (0 <= mntIoWaitPctList[x]['value'] <= 100)):
        print(mntIoWaitPctList[x]['name'] + ' odd number ' + str(mntIoWaitPctList[x]['value']))
      if (not (0 <= mntStealPctList[x]['value'] <= 100)):
        print(mntStealPctList[x]['name'] + ' odd number ' + str(mntStealPctList[x]['value']))

      #   print(mntIdlePctList[x]['name'] + ' decimals added :' + str(a.cpu_idle_pct + a.cpu_user_pct + a.cpu_system_pct + a.cpu_iowait_pct + a.cpu_steal_pct + a.cpu_irq_pct + a.cpu_guest_nice_pct + a.cpu_guest_pct ))
      # mntIdlePctList.pop(x)
      # mntUserPctList.pop(x)
      # mntSystemPctList.pop(x)
      # mntIoWaitPctList.pop(x)
      # mntStealPctList.pop(x)



    dataList.append({'name': 'User', 'series': mntUserPctList})
    dataList.append({'name': 'System', 'series': mntSystemPctList})
    dataList.append({'name': 'IO Waits', 'series': mntIoWaitPctList})
    dataList.append({'name': 'Steal', 'series': mntStealPctList})
    dataList.append({'name': 'Idle', 'series': mntIdlePctList})
    # Idle list must be appended last to be on the TOP of the graph

    graphData = json.dumps(dataList)

    return HttpResponse(graphData, status=status.HTTP_200_OK)
