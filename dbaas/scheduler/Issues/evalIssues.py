from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from djchoices import DjangoChoices

from dbaas.models import Server, CheckerThreshold, MetricNameChoices, Metrics_MountPoint


def IssuesFastTick():
    print('IssuesFastTick')
    # servers = Server.objects.filter(active_sw=True);
    #
    # for s in servers:
    #     print(s.server_name)
    #     metricThresholds = CheckerThreshold.objects.filter(active_sw=True, checker_base_element__active_sw=True).order_by('checker_base_elementk__metric_name', 'checker_base_element__metric_element')
    #     for m in metricThresholds:
    #         print(s.server_name + ':' + m.checker_base_element.metric_name + '-' + m.checker_base_element.metric_element)
    #         if m.checker_base_element.metric_name == MetricNameChoices.MountPoint:
    #             sm = MetricsMountPoint.objects.filter(server=s.id).latest('id')
    #             print(sm.mount_points +':' + sm.created_dttm + ',' + sm.used_pct);

