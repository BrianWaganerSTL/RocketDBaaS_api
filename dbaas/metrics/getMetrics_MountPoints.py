import requests
from django.utils import timezone

from dbaas.models import Metrics_MountPoint
from dbaas.trackers.track_mountpoints import Track_MountPoints

errCnt = [0] * 1000
metrics_port = 8080



def GetMetrics_MountPoints(server):
    print('Server='+str(server)+', ServerId='+str(server.id) + ', ServerIP=' + str(server.server_ip))

    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics/mountpoints'
    print('Check: MountPoints, ServerNm: ' + server.server_name + ', url=' + url)
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
        for m in metrics:
            print('m:' + str(m))

            metrics_MountPoint = Metrics_MountPoint()
            metrics_MountPoint.server = server
            metrics_MountPoint.error_cnt = errCnt[server.id]
            metrics_MountPoint.created_dttm = m['created_dttm']
            metrics_MountPoint.mount_point = m['mount_point']
            metrics_MountPoint.allocated_gb = m['allocated_gb']
            metrics_MountPoint.used_gb = m['used_gb']
            metrics_MountPoint.used_pct = m['used_pct']
            metrics_MountPoint.save()

            #try:
            #     print('metrics_MountPoint.id:' + metrics_MountPoint.id)
            #     Track_MountPoints(server, metrics_MountPoint.id)
            # except:
            #     print('ERROR: ' + str(e))
            #     pass
    else:
        metrics_MountPoint = Metrics_MountPoint()
        metrics_MountPoint.server = server
        metrics_MountPoint.error_cnt = errCnt[server.id]
        metrics_MountPoint.created_dttm = timezone.now()
        metrics_MountPoint.error_msg = error_msg
        metrics_MountPoint.save()

