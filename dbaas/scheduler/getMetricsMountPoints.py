# This calls out to the server to ask for the data, then pulls it back and saves it.
from datetime import datetime
import time
import os
import requests

from dbaas.models import MetricsMountPoint

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsMountPoints(s):
    metricsMountPoint = MetricsMountPoint()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/mountpoints'
    print('MountPoints: ServerNm: ' + s.server_name + ', url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        metricsMountPoint.server_id = s
        metricsMountPoint.created_dttm = metrics['created_dttm']
        metricsMountPoint.mount_point = metrics['mount_point']
        metricsMountPoint.allocated_gb = metrics['allocated_gb']
        metricsMountPoint.used_gb = metrics['used_gb']
        metricsMountPoint.used_pct = metrics['used_pct']
        metricsMountPoint.error_cnt = error_cnt
        metricsMountPoint.save()
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Timeout'
        metricsMountPoint.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Bad URL'
        metricsMountPoint.save()
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsMountPoint.save()
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Other Error ' + err
        metricsMountPoint.save()