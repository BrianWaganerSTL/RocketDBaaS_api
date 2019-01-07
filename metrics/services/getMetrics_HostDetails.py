import requests
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone

from RocketDBaaS.settings_local import MINION_PORT
from dbaas.models import Datacenter, Environment
from metrics.models import Metrics_HostDetail
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = MINION_PORT


def GetMetrics_HostDetails(server):
    server_ip = ''
    if (server.server_ip is None):
        if (server.server_name is None):
            return
        else:
            server_ip = server.server_name;
    else:
        server_ip = (server.server_ip).rstrip('\x00')

    url = 'http://' + server_ip + ':' + str(metrics_port) + '/minion_api/metrics/hostdetails'
    print('[HostDetails] Server=' + server.server_name + ', ServerId=' + str(server.id) + ', url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url)
        print('r.status_code:' + str(r.status_code))
        metrics = r.json()
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
            try:
                print('m:' + str(m))

                metrics_HostDetail = Metrics_HostDetail()
                metrics_HostDetail.server = server
                metrics_HostDetail.error_cnt = errCnt[server.id]
                metrics_HostDetail.created_dttm = m['created_dttm']
                metrics_HostDetail.ip_address = m['ipAddress']
                metrics_HostDetail.last_reboot = metrics['lastReboot']
                metrics_HostDetail.cpu = metrics['cpuCount']
                metrics_HostDetail.ram_gb = metrics['ramGb']
                metrics_HostDetail.db_gb = metrics['dbGb']
                metrics_HostDetail.os_version = metrics['osVersion']
                metrics_HostDetail.db_version = metrics['dbVersion']
                metrics_HostDetail.db_version_number = metrics['dbVersionNumber']
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

                if (server.db_gb is None) or (server.db_gb != m['dbGb']):
                    server.db_gb = m['dbGb'];
                    server.save()

                if (server.os_version is None) or (server.os_version != m['osVersion']):
                    server.os_version = m['osVersion'];
                    server.save()

                if (server.db_version is None) or (server.db_version != m['dbVersion']):
                    server.db_version = m['dbVersion'];
                    server.save()

                if (server.db_version_number is None) or (server.db_version_number != m['dbVersionNumber']):
                    server.db_version_number = m['dbVersionNumber'];
                    server.save()

                if (server.server_health is None):
                    server.server_health = server.ServerHealthChoices.ServerUp
                    server.save()

                if (server.datacenter is None):
                    dc = Datacenter()
                    if (server.server_name.find('ch')):
                        dc = get_object_or_404(Datacenter.objects.get(datacenter='CH'));
                        server.datacenter = dc
                    else:
                        dc = get_object_or_404(Datacenter.objects.get(datacenter='PA'));
                        server.datacenter = dc
                    server.save()

                if (server.environment is None):
                    env = Environment()
                    envChars = server.server_name[3:4]
                    if   (envChars == 'x'):
                        env = get_object_or_404(Environment.objects.filter(env_name='Sbx'))
                        server.environment = env
                    elif (envChars == 'd'):
                        env = get_object_or_404(Environment.objects.filter(env_name='Dev'))
                        server.environment = env
                    elif (envChars == 'q'):
                        env = get_object_or_404(Environment.objects.filter(env_name='QA'))
                        server.environment = env
                    elif (envChars == 'u'):
                        env = get_object_or_404(Environment.objects.filter(env_name='UAT'))
                        server.environment = env
                    elif (envChars == 'p'):
                        env = get_object_or_404(Environment.objects.filter(env_name='Prod'))
                        server.environment = env
                    server.save()

                try:
                    MetricThresholdTest(server, 'HostDetails', 'lastReboot', metrics_HostDetail.lastReboot, '')
                except:
                    pass
            except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
                print('Error: ' + str(ex))
    else:
        metrics_HostDetail = Metrics_HostDetail()
        metrics_HostDetail.server = server
        metrics_HostDetail.error_cnt = errCnt[server.id]
        metrics_HostDetail.created_dttm = timezone.now()
        metrics_HostDetail.error_msg = error_msg
        metrics_HostDetail.save()
