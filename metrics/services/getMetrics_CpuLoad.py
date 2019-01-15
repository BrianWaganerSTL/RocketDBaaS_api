import requests
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone

from RocketDBaaS.settings_local import MINION_PORT
from metrics.models import Metrics_CpuLoad
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = MINION_PORT


def GetMetrics_Load(server):
    if (server.server_ip is None):
        return

    server_ip = (server.server_ip).rstrip('\x00')

    url = 'http://' + server_ip + ':' + str(metrics_port) + '/minion_api/metrics/load'
    print('\n[CpuLoad] Server=' + server.server_name + ', ServerId=' + str(server.id) + ', url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url)
        print('r.status_code:' + str(r.status_code))
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
    except:
        print('ERROR: Other')

    if (error_msg == ''):
        if (type(metrics) == dict):
            metricsList = [metrics]
        else:
            metricsList = metrics

        for m in metricsList:
            try:
                print('m:' + str(m))
                metrics_CpuLoad = Metrics_CpuLoad()
                metrics_CpuLoad.server = server
                metrics_CpuLoad.error_cnt = errCnt[server.id]
                metrics_CpuLoad.created_dttm = m['created_dttm']
                metrics_CpuLoad.load_1min = m['load_1min']
                metrics_CpuLoad.load_5min = m['load_5min']
                metrics_CpuLoad.load_15min = m['load_15min']
                metrics_CpuLoad.save()
                print('Post Save')

                try:
                     MetricThresholdTest(server, 'CpuLoad', 'load_1min', metrics_CpuLoad.load_1min, '')
                     print('Post MetricThresholdTest 1min')
                except:
                     print('ERROR: ' + str(e))
                     pass

                try:
                     MetricThresholdTest(server, 'CpuLoad', 'load_5min', metrics_CpuLoad.load_5min, '')
                     print('Post MetricThresholdTest 5min')
                except:
                     print('ERROR: ' + str(e))
                     pass

            except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
                print('Error: ' + str(ex))
    else:
        metrics_CpuLoad = Metrics_CpuLoad()
        metrics_CpuLoad.server = server
        metrics_CpuLoad.error_cnt = errCnt[server.id]
        metrics_CpuLoad.created_dttm = timezone.now()
        metrics_CpuLoad.error_msg = error_msg
        metrics_CpuLoad.save()
