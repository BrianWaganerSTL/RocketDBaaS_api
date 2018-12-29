import requests
from django.utils import timezone

from metrics.models import Metrics_Cpu
from monitor.services.metric_threshold_test import MetricThresholdTest


errCnt = [0] * 1000
metrics_port = 8080


def GetMetrics_Cpu(server):
    print('Server=' + str(server) + ', ServerId=' + str(server.id) + ', ServerIP=' + str(server.server_ip))

    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics_temp/cpu'
    print('Cpu: ServerNm: ' + server.server_name + ', url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url)
        print('r.status_code:' + str(r.status_code))
        print('r.' + str(r.content))
        metrics = r.json()
        print("metrics_temp" + str(type(metrics)) + ', Count=' + str(len(metrics)))
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

            metrics_Cpu = Metrics_Cpu()
            metrics_Cpu.server = server
            metrics_Cpu.error_cnt = errCnt[server.id]
            metrics_Cpu.created_dttm = m['created_dttm']
            metrics_Cpu.cpu_idle_pct = metrics['idle']
            metrics_Cpu.cpu_user_pct = metrics['user']
            metrics_Cpu.cpu_system_pct = metrics['system']
            if 'cpu_iowait_pct' in metrics:  # These only exist in Unix/Linux
                metrics_Cpu.cpu_iowait_pct = metrics['cpu_iowait_pct']
                metrics_Cpu.cpu_irq_pct = metrics['cpu_irq_pct']
                metrics_Cpu.cpu_steal_pct = metrics['cpu_steal_pct']
                if 'cpu_guest_pct' in metrics:  # Only certain versions of Unix/Linux has
                    metrics_Cpu.cpu_guest_pct = metrics['cpu_guest_pct']
                    metrics_Cpu.cpu_guest_nice_pct = metrics['cpu_guest_nice_pct']
            metrics_Cpu.save()

            try:
                MetricThresholdTest(server, 'Cpu', 'cpu_idle_pct', metrics_Cpu.cpu_idle_pct, '')
            except:
                 print('ERROR: ' + str(e))
                 pass
    else:
        metrics_Cpu = Metrics_Cpu()
        metrics_Cpu.server = server
        metrics_Cpu.error_cnt = errCnt[server.id]
        metrics_Cpu.created_dttm = timezone.now()
        metrics_Cpu.error_msg = error_msg
        metrics_Cpu.save()
