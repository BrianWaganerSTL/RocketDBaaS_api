import os
from django.utils import timezone
from sys import platform

from dbaas.models import MetricsPingServer

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsPingServer(s):
    print('PingServer: ping')

    if platform == "linux" or platform =="linux2":
        pingCmd = 'ping -c1 -W2 ' + s.server_ip
    elif platform == "darwin":  # Mac OS
        pingCmd = 'ping -c1 -W2 ' + s.server_ip
    elif platform == "win32":
        pingCmd = 'ping -n 1 -w 2 ' + s.server_ip

    metricsPingServer = MetricsPingServer()

    startTs = timezone.now()
    response = os.system(pingCmd)
    stopTs = timezone.now()

    if response == 0:
        errCnt[s.id] = 0
        pingStatus = 'Normal'
        errorMsg = ''

    else:
        errCnt[s.id] = errCnt[s.id] + 1
        pingStatus = 'Critical'
        errorMsg = 'Server not available'

    metricsPingServer.server_id = s
    metricsPingServer.created_dttm = timezone.now()
    metricsPingServer.ping_status = pingStatus
    metricsPingServer.ping_response_ms = int((stopTs - startTs).total_seconds()*1000)
    metricsPingServer.error_cnt = errCnt[s.id]
    metricsPingServer.error_msg = errorMsg
    metricsPingServer.save()
