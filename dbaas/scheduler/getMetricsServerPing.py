from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsServerPing

errCnt = [0] * 1000
metrics_port = 8080


def GetServerMetricsPing(s):
    metricsServerPing = MetricsServerPing()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/cpu?server_id=' + str(s.id)
    print('ServerNm: ' + s.server_name + ', url=' + url)

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

    metricsServerPing.server_id = s
    metricsServerPing.created_dttm = timezone.now()
    metricsServerPing.db_ping_status = pingStatus
    metricsServerPing.db_ping_response_ms = int((stopTs - startTs).total_seconds()*1000)
    metricsServerPing.error_cnt = errCnt[s.id]
    metricsServerPing.error_msg = errorMsg
    metricsServerPing.save()
