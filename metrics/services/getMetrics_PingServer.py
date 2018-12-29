import os
from django.utils import timezone
from sys import platform

from metrics.models import Metrics_PingServer
from monitor.services.metric_threshold_test import MetricThresholdTest


errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsPingServer(server):
    print('PingServer: ping')

    if platform == "linux" or platform =="linux2":
        pingCmd = 'ping -c1 -W2 ' + server.server_ip
    elif platform == "darwin":  # Mac OS
        pingCmd = 'ping -c1 -W2 ' + server.server_ip
    elif platform == "win32":
        pingCmd = 'ping -n 1 -w 2 ' + server.server_ip

    metrics_PingServer = Metrics_PingServer()

    startTs = timezone.now()
    response = os.system(pingCmd)
    stopTs = timezone.now()

    if response == 0:
        errCnt[server.id] = 0
        pingStatus = 'Normal'
        errorMsg = ''

    else:
        errCnt[server.id] = errCnt[server.id] + 1
        pingStatus = 'Critical'
        errorMsg = 'Server not available'

    metrics_PingServer.server = server
    metrics_PingServer.created_dttm = timezone.now()
    metrics_PingServer.ping_status = pingStatus
    metrics_PingServer.ping_response_ms = int((stopTs - startTs).total_seconds()*1000)
    metrics_PingServer.error_cnt = errCnt[server.id]
    metrics_PingServer.error_msg = errorMsg
    metrics_PingServer.save()

    try:
        MetricThresholdTest(server, 'PingServer', 'ping_response_ms', metrics_PingServer.ping_response_ms, '')
    except:
        print('ERROR: ' + str(e))
        pass
