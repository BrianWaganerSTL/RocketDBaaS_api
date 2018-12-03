from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsPingServer

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsPingServer(s):
    metricsPingServer = MetricsPingServer()
    print('PingServer: ping')
    startTs = timezone.now()
    response = os.system("ping -w 2 " + s.server_ip)
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
    print('ping_status=' + pingStatus + ', response_ms=' +str(int((stopTs - startTs).total_seconds()*1000)))
    metricsPingServer.save()
