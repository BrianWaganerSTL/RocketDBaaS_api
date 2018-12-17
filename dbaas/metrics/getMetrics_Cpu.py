# This calls out to the server to ask for the data, then pulls it back and saves it.
from datetime import datetime
import time
import os
import requests

from dbaas.models import MetricsCpu

errCnt = [0] * 1000
metrics_port = 8080


def GetMetricsCpu(s):
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/cpu'
    print('Cpu: ServerNm: ' + s.server_name + ', url=' + url)

    metricsCpu = MetricsCpu()
    error_msg = ''
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        errCnt[s.id] = errCnt[s.id] = 0
        metricsCpu.created_dttm = metrics['created_dttm']
        metricsCpu.cpu_idle_pct = metrics['idle']
        metricsCpu.cpu_user_pct = metrics['user']
        metricsCpu.cpu_system_pct = metrics['system']
        if 'cpu_iowait_pct' in metrics:  # These only exist in Unix/Linux
            metricsCpu.cpu_iowait_pct = metrics['cpu_iowait_pct']
            metricsCpu.cpu_irq_pct = metrics['cpu_irq_pct']
            metricsCpu.cpu_steal_pct = metrics['cpu_steal_pct']
            if 'cpu_guest_pct' in metrics:  # Only certain versions of Unix/Linux has
                metricsCpu.cpu_guest_pct = metrics['cpu_guest_pct']
                metricsCpu.cpu_guest_nice_pct = metrics['cpu_guest_nice_pct']
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        error_msg = 'Timeout'
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        error_msg = 'Bad URL'
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        error_msg = 'Catastrophic error. Bail ' + str(e)
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        error_msg = 'Other Error ' + err

    metricsCpu.error_msg = error_msg
    metricsCpu.error_cnt = errCnt[s.id]
    metricsCpu.server = s
    metricsCpu.save()
