from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsPingDb
from dbaas.trackers.track_ping_db import Track_PingDb

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsPingDb(server):
    print('Server=' + str(server) + ', ServerId=' + str(server.id) + ', ServerIP=' + str(server.server_ip))

    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics/pingdb?dbms=PostgreSQL'
    print('PingDb: url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url)
        print('r.status_code:' + str(r.status_code))
        print('r.' + str(r.content))
        metrics = r.json()
        print("metrics" + str(type(metrics)) + ', Count=' + str(len(metrics)))
        print(metrics)
        errCnt[server.id] = 0

    except requests.exceptions.ConnectionError:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'ConnectionRefusedError:  Make sure the Minion is up and running.'
    except requests.exceptions.Timeout:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Timeout'
    except requests.exceptions.TooManyRedirects:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Bad URL'
    except requests.exceptions.RequestException as e:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Catastrophic error. Bail ' + str(e)
    except requests.exceptions.HTTPError as err:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Other Error ' + err

    if (error_msg == ''):
        if (type(metrics) == dict):
            metricsList = [metrics]
        else:
            metricsList = metrics

        for m in metricsList:
            print('m:' + str(m))

            metricsPingDb = MetricsPingDb()
            metricsPingDb.server = server
            metricsPingDb.error_cnt = errCnt[server.id]
            metricsPingDb.created_dttm = m['created_dttm']
            metricsPingDb.ping_db_status = metrics['ping_db_status']
            metricsPingDb.ping_db_response_ms = metrics['ping_db_response_ms']
            metricsPingDb.save()

            try:
                 Track_PingDb(server, metricsPingDb.id)
            except:
                 print('ERROR: ' + str(e))
                 pass
    else:
        metricsPingDb = MetricsPingDb()
        metricsPingDb.server = server
        metricsPingDb.error_cnt = errCnt[server.id]
        metricsPingDb.created_dttm = timezone.now()
        metricsPingDb.error_msg = error_msg
        metricsPingDb.save()
