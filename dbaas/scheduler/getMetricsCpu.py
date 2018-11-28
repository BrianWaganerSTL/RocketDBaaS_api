from datetime import datetime
import time
import os
import requests

from dbaas.models import MetricsCpu

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsCpu(s):
    metricsCpu = MetricsCpu()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/cpu?server_id=' + str(s.id)
    print('ServerNm: ' + s.server_name + ', url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        error_msg = ''
        metricsCpu.server_id = s
        metricsCpu.cpu_idle_pct = metrics['idle']
        metricsCpu.cpu_user_pct = metrics['user']
        metricsCpu.cpu_system_pct = metrics['system']
        metricsCpu.cpu_iowait_pct = metrics.get('cpu_iowait_pct') or 0
        metricsCpu.cpu_irq_pct = metrics.get('cpu_irq_pct') or 0
        metricsCpu.cpu_steal_pct = metrics.get('cpu_steal_pct') or 0
        metricsCpu.cpu_guest_pct = metrics.get('cpu_guest_pct') or 0
        metricsCpu.cpu_guest_nice_pct = metrics.get('cpu_guest_nice_pct') or 0
        metricsCpu.error_cnt = error_cnt
        metricsCpu.save()
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsCpu.server_id = s
        metricsCpu.error_cnt = errCnt[s.id]
        metricsCpu.error_msg = 'Timeout'
        metricsCpu.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsCpu.server_id = s
        metricsCpu.error_cnt = errCnt[s.id]
        metricsCpu.error_msg = 'Bad URL'
        metricsCpu.save()
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsCpu.server_id = s
        metricsCpu.error_cnt = errCnt[s.id]
        metricsCpu.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsCpu.save()
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsCpu.server_id = s
        metricsCpu.error_cnt = errCnt[s.id]
        metricsCpu.error_msg = 'Other Error ' + err
        metricsCpu.save()