from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from djchoices import DjangoChoices

from dbaas.models import Server, MetricThreshold, MetricNameChoices, MetricsMountPoint


def IssuesFastTick():
    print('IssuesFastTick')
    # servers = Server.objects.filter(active_sw=True);
    #
    # for s in servers:
    #     print(s.server_name)
    #     metricThresholds = MetricThreshold.objects.filter(active_sw=True, metric_check__active_sw=True).order_by('metric_check__metric_name', 'metric_check__metric_element')
    #     for m in metricThresholds:
    #         print(s.server_name + ':' + m.metric_check.metric_name + '-' + m.metric_check.metric_element)
    #         if m.metric_check.metric_name == MetricNameChoices.MountPoint:
    #             sm = MetricsMountPoint.objects.filter(server_id=s.id).latest('id')
    #             print(sm.mount_points +':' + sm.created_dttm + ',' + sm.used_pct);

