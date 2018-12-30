import requests
from django.utils import timezone

from metrics.models import Metrics_PingDb, Metrics_HostDetails
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = 8080


def GetMetrics_HostDetails(server):
    if (server.server_ip is None):
        return

    server_ip = (server.server_ip).rstrip('\x00')

    print('Server=' + server + ', ServerId=' + str(server.id) + ', ServerIP=' + server_ip)

    url = 'http://' + server_ip + ':' + str(metrics_port) + '/api/metrics/hostdetails'
    print('hostdetails: url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url)
        print('r.status_code:' + str(r.status_code))
        print('r.' + str(r.content))
        metrics = r.json()
        print("metrics" + str(type(metrics)))
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

            metrics_HostDetails = Metrics_HostDetails()
            metrics_HostDetails.server = server
            metrics_HostDetails.error_cnt = errCnt[server.id]
            metrics_HostDetails.created_dttm = m['created_dttm']
            metrics_HostDetails.cpuCount = metrics['cpuCount']
            metrics_HostDetails.lastReboot = metrics['lastReboot']
            metrics_HostDetails.ramGb = metrics['ramGb']
            metrics_HostDetails.osVersion = metrics['osVersion']
            metrics_HostDetails.dbVersion = metrics['dbVersion']
            metrics_HostDetails.save()

            try:
                MetricThresholdTest(server, 'HostDetails', 'lastReboot', metrics_HostDetails.lastReboot, '')
            except:
                 print('ERROR: ' + str(e))
                 pass
    else:
        metrics_HostDetails = Metrics_HostDetails()
        metrics_HostDetails.server = server
        metrics_HostDetails.error_cnt = errCnt[server.id]
        metrics_HostDetails.created_dttm = timezone.now()
        metrics_HostDetails.error_msg = error_msg
        metrics_HostDetails.save()
