from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsLoad

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsLoad(s):
    metricsLoad = MetricsLoad()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/load'
    print('Load: url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        metricsLoad.server = s
        metricsLoad.created_dttm = metrics['created_dttm']
        metricsLoad.load_1min = metrics['load_1min']
        metricsLoad.load_5min = metrics['load_5min']
        metricsLoad.load_15min = metrics['load_15min']
        metricsLoad.error_cnt = error_cnt
        metricsLoad.save()
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsLoad.server = s
        metricsLoad.error_cnt = errCnt[s.id]
        metricsLoad.error_msg = 'Timeout'
        metricsLoad.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsLoad.server = s
        metricsLoad.error_cnt = errCnt[s.id]
        metricsLoad.error_msg = 'Bad URL'
        metricsLoad.save()
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsLoad.server = s
        metricsLoad.error_cnt = errCnt[s.id]
        metricsLoad.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsLoad.save()
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsLoad.server = s
        metricsLoad.error_cnt = errCnt[s.id]
        metricsLoad.error_msg = 'Other Error ' + err
        metricsLoad.save()
