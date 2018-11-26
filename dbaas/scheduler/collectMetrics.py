"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.urlparse
"""

from datetime import datetime
import time
import os
import requests

from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import get_object_or_404
from django.utils import timezone

from dbaas.models import Server, MetricsCpu

errCnt=[0]*1000


def Tick():
    # print('Tick! The time is: %s' % datetime.now())
    metrics_port = 8080
    servers = Server.objects.filter(active_sw=True).filter(metrics_sw=True);
    metricsCpu = MetricsCpu()

    for s in servers:
        url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/cpu?server_id=' + str(s.id)
        print('ServerNm: ' + s.server_name + ', url=' + url)
        try:
            r = requests.get(url)
            metrics = r.json()
            print(metrics)

            metricsCpu.server_id = s
            metricsCpu.created_dttm = metrics['created_dttm']
            metricsCpu.cpu_user_pct = metrics['user']
            metricsCpu.cpu_system_pct = metrics['system']
            metricsCpu.cpu_idle_pct = metrics['idle']
            metricsCpu.save()
        except requests.exceptions.Timeout:
            errCnt[s.id] = errCnt[s.id]+1
            print(s.server_name + ') Maybe set up for a retry, or continue in a retry loop. Error Count: ' + str(errCnt[s.id]) )
        except requests.exceptions.TooManyRedirects:
            errCnt[s.id] = errCnt[s.id] + 1
            print(s.server_name + ') Tell the user their URL was bad and try a different one. Error Count: ' + str(errCnt[s.id]) )
        except requests.exceptions.RequestException as e:
            errCnt[s.id] = errCnt[s.id] + 1
            print(s.server_name + ') catastrophic error. bail. Error Count: ' + str(errCnt[s.id]) )
            print(e)
            # Check if it is pingable
            response = os.system("ping -w 2 " + s.server_ip)
            print(response)
            if response == 0:
                print(s.server_name + ' is reachable')
            else:
                print(s.server_name + ' is unreachable')
        except requests.exceptions.HTTPError as err:
            errCnt[s.id] = errCnt[s.id] + 1
            print(s.server_name + ') ' + err +' Error Count: ' + str(errCnt[s.id]) )
            # Check if it is pingable
            response = os.system("ping -w 2 " + s.server_ip + " 2>/dev/null")
            print(response)
            if response == 0:
                print(s.server_name + ' is reachable')
            else:
                print(s.server_name + ' is unreachable')

class StartSchedule():
    scheduler = BackgroundScheduler()
    scheduler.add_job(Tick, 'interval', seconds=30, max_instances=10, next_run_time=timezone.now())
    scheduler.start()
