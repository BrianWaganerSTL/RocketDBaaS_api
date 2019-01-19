from decimal import Decimal

import requests
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone

from RocketDBaaS.settings_local import MINION_PORT
from metrics.models import Metrics_MountPoint
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = MINION_PORT


def GetMetrics_MountPoints(server):
    if (server.server_ip is None):
        return

    server_ip = (server.server_ip).rstrip('\x00')
    url = ('http://' + server_ip + ':' + str(metrics_port) + '/minion_api/metrics/mountpoints').rstrip('\x00')
    print('\n[MountPoints] ServerNm: ' + server.server_name + ', url=' + url)
    metrics = ''
    error_msg = ''

    try:
        r = requests.get(url, params={'timeout': 10})
        metrics = r.json()
        print("metrics" + str(type(metrics)) + ', Count=' + str(len(metrics)) + ', r.status_code:' + str(r.status_code))
        print(metrics)
        errCnt[server.id] = 0
    except requests.exceptions.ConnectionError:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'ConnectionRefusedError:  Make sure the Minion is up and running.'
        print(error_msg)
    except requests.exceptions.Timeout:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Timeout'
        print(error_msg)
    except requests.exceptions.TooManyRedirects:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Bad URL'
        print(error_msg)
    except requests.exceptions.RequestException as e:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Catastrophic error. Bail ' + str(e)
        print(error_msg)
    except requests.exceptions.HTTPError as err:
        errCnt[server.id] = errCnt[server.id] + 1
        error_msg = 'Other Error ' + err
        print(error_msg)
    except:
        print('ERROR: Other')

    if (error_msg == ''):
        for m in metrics:
            try:
                print('m:' + str(m))

                metrics_MountPoint = Metrics_MountPoint()
                metrics_MountPoint.server = server
                metrics_MountPoint.error_cnt = errCnt[server.id]
                metrics_MountPoint.created_dttm = m['created_dttm']
                metrics_MountPoint.mount_point = m['mount_point']
                metrics_MountPoint.allocated_gb = Decimal(m['allocated_gb'])
                metrics_MountPoint.used_gb = Decimal(m['used_gb'])
                metrics_MountPoint.used_pct = Decimal(m['used_pct'])
                metrics_MountPoint.save()

                try:
                     MetricThresholdTest(server, 'MountPoint', 'used_pct', metrics_MountPoint.used_pct, metrics_MountPoint.mount_point)
                except:
                     print('ERROR: ' + str(e))
                     pass
            except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
                print('Error: ' + str(ex))
    else:
        metrics_MountPoint = Metrics_MountPoint()
        metrics_MountPoint.server = server
        metrics_MountPoint.error_cnt = errCnt[server.id]
        metrics_MountPoint.created_dttm = timezone.now()
        metrics_MountPoint.error_msg = error_msg
        metrics_MountPoint.save()

