import requests
from django.utils import timezone
import pytz

from dbaas.models import Datacenter, Environment
from metrics.models import Metrics_PingDb, Metrics_HostDetail
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = 8080


def GetMetrics_HostDetails(server):
    if (server.server_ip is None):
        if (server.server_name is None):
            return
        else:
            server_ip = server.server_name;
    else:
        server_ip = (server.server_ip).rstrip('\x00')

    print('[HostDetails]Server=' + server.server_name + ', ServerId=' + str(server.id) + ', ServerIP=' + server_ip)
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

            metrics_HostDetail = Metrics_HostDetail()
            metrics_HostDetail.server = server
            metrics_HostDetail.error_cnt = errCnt[server.id]
            metrics_HostDetail.created_dttm = m['created_dttm']
            metrics_HostDetail.ip_address = m['ipAddress']
            metrics_HostDetail.last_reboot = metrics['lastReboot']
            metrics_HostDetail.cpu = metrics['cpuCount']
            metrics_HostDetail.ram_gb = metrics['ramGb']
            metrics_HostDetail.os_version = metrics['osVersion']
            metrics_HostDetail.db_version = metrics['dbVersion']
            metrics_HostDetail.save()

            if (server.server_ip is None) and (m['ipAddress'] != ''):
                server.server_ip = m['ipAddress'];
                server.save()
            if (server.last_reboot is None) or (server.last_reboot != m['lastReboot']):
                server.last_reboot = m['lastReboot'];
                server.save()
            if (server.cpu is None) or (server.cpu != m['cpuCount']):
                server.cpu = m['cpuCount'];
                server.save()
            if (server.ram_gb is None) or (server.ram_gb != m['ramGb']):
                server.ram_gb = m['ramGb'];
                server.save()
            if (server.os_version is None) or (server.os_version != m['osVersion']):
                server.os_version = m['osVersion'];
                server.save()
            if (server.db_version is None) or (server.db_version != m['dbVersion']):
                server.db_version = m['dbVersion'];
                server.save()
            if (server.server_health is None):
                server.server_health = server.ServerHealthChoices.ServerUp
                server.save()
            if (server.datacenter is None):
                if (server.server_name.find('CH')):
                    dc = Datacenter.objects.get(datacenter='CH');
                    server.datacenter = dc
                else:
                    dc = Datacenter.objects.get(datacenter='PA');
                    server.datacenter = dc
                server.save()
            if (server.environment is None):
                envChars = server.server_name[3:4]
                if   (envChars == 'x'):
                    server.environment = Environment.objects.get(Environment.env_name=="Sbx");
                elif (envChars == 'd'):
                    server.environment = Environment.objects.get(Environment.env_name=="Dev");
                elif (envChars == 'q'):
                    server.environment = Environment.objects.get(Environment.env_name=="QA");
                elif (envChars == 'u'):
                    server.environment = Environment.objects.get(Environment.env_name=="UAT");
                elif (envChars == 'p'):
                    server.environment = Environment.objects.get(Environment.env_name=="Prod");
                server.save()
            try:
                MetricThresholdTest(server, 'HostDetails', 'lastReboot', metrics_HostDetail.lastReboot, '')
            except:
                pass
    else:
        metrics_HostDetail = Metrics_HostDetail()
        metrics_HostDetail.server = server
        metrics_HostDetail.error_cnt = errCnt[server.id]
        metrics_HostDetail.created_dttm = timezone.now()
        metrics_HostDetail.error_msg = error_msg
        metrics_HostDetail.save()
