from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsPingDb

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsPingDb(s):
    metricsPingDb = MetricsPingDb()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/pingdb?dbms=PostgreSQL'
    print('PingDb: url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        metricsPingDb.server = s
        metricsPingDb.created_dttm = metrics['created_dttm']
        metricsPingDb.ping_db_status = metrics['ping_db_status']
        metricsPingDb.ping_db_response_ms = metrics['ping_db_response_ms']
        metricsPingDb.error_cnt = error_cnt
        metricsPingDb.save()
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsPingDb.server = s
        metricsPingDb.error_cnt = errCnt[s.id]
        metricsPingDb.error_msg = 'Timeout'
        metricsPingDb.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsPingDb.server = s
        metricsPingDb.error_cnt = errCnt[s.id]
        metricsPingDb.error_msg = 'Bad URL'
        metricsPingDb.save()
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsPingDb.server = s
        metricsPingDb.error_cnt = errCnt[s.id]
        metricsPingDb.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsPingDb.save()
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsPingDb.server = s
        metricsPingDb.error_cnt = errCnt[s.id]
        metricsPingDb.error_msg = 'Other Error ' + err
        metricsPingDb.save()
