from datetime import datetime
import time
import os
import requests
from django.utils import timezone

from dbaas.models import MetricsLoad
from dbaas.trackers.track_load import Track_Load

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsLoad(server):
    print('Server=' + str(server) + ', ServerId=' + str(server.id) + ', ServerIP=' + str(server.server_ip))

    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics/load'
    print('Load: url=' + url)
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

            metricsLoad = MetricsLoad()
            metricsLoad.server = server
            metricsLoad.error_cnt = errCnt[server.id]
            metricsLoad.created_dttm = m['created_dttm']
            metricsLoad.load_1min = m['load_1min']
            metricsLoad.load_5min = m['load_5min']
            metricsLoad.load_15min = m['load_15min']
            metricsLoad.save()

            try:
                 print('metricsLoad.id: ' + str(metricsLoad.id))
                 Track_Load(server, metricsLoad.id)
            except:
                 print('ERROR: ' + str(e))
                 pass
    else:
        metricsLoad = MetricsLoad()
        metricsLoad.server = server
        metricsLoad.error_cnt = errCnt[server.id]
        metricsLoad.created_dttm = timezone.now()
        metricsLoad.error_msg = error_msg
        metricsLoad.save()
