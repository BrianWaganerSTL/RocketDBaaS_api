import requests
from django.utils import timezone

from dbaas.models import Metrics_MountPoint
from dbaas.trackers.track_mountpoints import Track_MountPoints

errCnt = [0] * 1000
metrics_port = 8080



def GetMetrics_MountPoints(server):
    print('Server='+str(server)+', ServerId='+str(server.id) + ', ServerIP=' + str(server.server_ip))
    metrics_MountPoint = Metrics_MountPoint()
    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics/mountpoints'
    print('Check: MountPoints, ServerNm: ' + server.server_name + ', url=' + url)
    metrics = ''

    try:
        r = requests.get(url)
        metrics = r.json()
        errCnt[server.id] = 0
    except requests.exceptions.ConnectionError:
        errCnt[server.id] = errCnt[server.id] + 1
        metrics_MountPoint.error_msg = 'ConnectionRefusedError:  Make sure the Minion is up and running.'
    except requests.exceptions.Timeout:
        errCnt[server.id] = errCnt[server.id] + 1
        metrics_MountPoint.error_msg = 'Timeout'
    except requests.exceptions.TooManyRedirects:
        errCnt[server.id] = errCnt[server.id] + 1
        metrics_MountPoint.error_msg = 'Bad URL'
    except requests.exceptions.RequestException as e:
        errCnt[server.id] = errCnt[server.id] + 1
        metrics_MountPoint.error_msg = 'Catastrophic error. Bail ' + str(e)
    except:
        errCnt[server.id] = errCnt[server.id] + 1
        metrics_MountPoint.error_msg = 'Other Error '

    metrics_MountPoint.server = server
    metrics_MountPoint.error_cnt = errCnt[server.id]
    if (metrics_MountPoint.error_msg == ''):
        metrics_MountPoint.created_dttm = metrics['created_dttm']
        metrics_MountPoint.mount_point = metrics['mount_point']
        metrics_MountPoint.allocated_gb = metrics['allocated_gb']
        metrics_MountPoint.used_gb = metrics['used_gb']
        metrics_MountPoint.used_pct = metrics['used_pct']
        metrics_MountPoint.save()

        Track_MountPoints(server, metrics_MountPoint.id)
    else:
        metrics_MountPoint.created_dttm = timezone.now()
        metrics_MountPoint.save()

