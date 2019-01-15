import requests
from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone

from RocketDBaaS.settings_local import MINION_PORT
from metrics.models import Metrics_PingDb
from monitor.services.metric_threshold_test import MetricThresholdTest

errCnt = [0] * 1000
metrics_port = MINION_PORT


def GetMetrics_PingDb(server):

    if (server.server_ip is None):
        return

    server_ip = (server.server_ip).rstrip('\x00')

    if (server.dbms_type is None):
        return
    if (server.dbms_type != 'PostgreSQL'):
        return

    url = 'http://' + server_ip + ':' + str(metrics_port) + '/minion_api/metrics/pingdb?dbms=' + server.dbms_type
    print('\n[PingDb] Server=' + server.server_name + ', ServerId=' + str(server.id) + ', url=' + url)
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
                metrics_PingDb = Metrics_PingDb()
                metrics_PingDb.server = server
                metrics_PingDb.error_cnt = errCnt[server.id]
                metrics_PingDb.created_dttm = m['created_dttm']
                metrics_PingDb.ping_db_status = metrics['ping_db_status']
                metrics_PingDb.ping_db_response_ms = metrics['ping_db_response_ms']
                metrics_PingDb.save()

                try:
                    MetricThresholdTest(server, 'PingDb', 'ping_db_response_ms', metrics_PingDb.ping_db_response_ms, '')
                except:
                     print('ERROR: ' + str(e))
                     pass
            except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
                print('Error: ' + str(ex))

    else:
        metrics_PingDb = Metrics_PingDb()
        metrics_PingDb.server = server
        metrics_PingDb.error_cnt = errCnt[server.id]
        metrics_PingDb.created_dttm = timezone.now()
        metrics_PingDb.error_msg = error_msg
        metrics_PingDb.save()
