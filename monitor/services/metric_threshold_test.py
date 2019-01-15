from django.utils import timezone

from dbaas.models import Server
from monitor.models import ThresholdTest, IncidentStatusChoices, Incident, IncidentNotification
from dbaas.utils.DynCompare import DynCompare
from django.utils import timezone

from dbaas.models import Server
from dbaas.utils.DynCompare import DynCompare
from monitor.models import ThresholdTest, IncidentStatusChoices, Incident, IncidentNotification


def MetricThresholdTest(slimServer, category_name, metric_name, metric_value, detail_element):
    server = Server.objects.get(id=slimServer.id)
    try:
        thresholdTest = ThresholdTest.objects \
            .filter(active_sw=True,
                    threshold_metric__category__category_name=category_name,
                    threshold_metric__metric_name=metric_name)[0]
    except:
        print('Found no active ThresholdTest for ' + category_name + ' (' + metric_name + ')')
        return
    else:
        critical_value = eval(thresholdTest.critical_value.replace("<<CPU>>", str(server.cpu)))
        warning_value = eval(thresholdTest.critical_value.replace("<<CPU>>", str(server.cpu)))
        if DynCompare(metric_value, thresholdTest.critical_predicate_type, critical_value):
            pendingThresholdLevel = IncidentStatusChoices.Critical
            CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.critical_predicate_type, thresholdTest.critical_value)
        elif DynCompare(metric_value, thresholdTest.warning_predicate_type, warning_value):
            pendingThresholdLevel = IncidentStatusChoices.Warning
            CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, thresholdTest.warning_value)
        else:
            pendingThresholdLevel = IncidentStatusChoices.Normal
            CurTestWithValues = '%d NOT (Warning OR Critical)' % (metric_value)

        print('Pending %s Threshold' % pendingThresholdLevel)

    #  Now Create an Incident if one doesn't already exist
    twerkIt = False
    try:
        i = Incident.objects.filter(server_id=server.id, threshold_test=thresholdTest, closed_sw=False)[0]
    except:
        if (pendingThresholdLevel in ['Critical', 'Warning']):
            i = Incident(server_id=server.id, threshold_test=thresholdTest, pending_status=pendingThresholdLevel)
            print('Created a Incident')
        else:
            return

    i.detail_element = detail_element
    i.cur_test_w_values = CurTestWithValues
    i.cur_value = metric_value
    if (metric_value > i.max_value):
        i.max_value = metric_value
    if (metric_value < i.min_value):
        i.min_value = metric_value

    i.last_dttm = timezone.now()
    i.save()  # Save so I get the datetimes and other default

    if pendingThresholdLevel == 'Critical':
        i.critical_ticks = min(i.critical_ticks + 1, thresholdTest.critical_ticks)
        i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
        i.normal_ticks = max(i.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (thresholdTest.critical_ticks, i.critical_ticks))
        if (i.critical_ticks == thresholdTest.critical_ticks):
            if (i.pending_status != i.current_status):
                twerkIt = True
                i.current_status = i.pending_status
            i.pending_status = IncidentStatusChoices.Critical

    elif pendingThresholdLevel == 'Warning':
        i.critical_ticks = max(i.critical_ticks - 1, 0)
        i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
        i.normal_ticks = max(i.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (thresholdTest.warning_ticks, i.warning_ticks))
        if (i.warning_ticks == thresholdTest.warning_ticks):
            if (i.pending_status != i.current_status):
                twerkIt = True
                i.current_status = i.pending_status
            i.current_status = IncidentStatusChoices.Warning

    elif pendingThresholdLevel == 'Normal':
        i.critical_ticks = max(i.critical_ticks - 1, 0)
        i.warning_ticks = max(i.warning_ticks - 1, 0)
        i.normal_ticks = min(i.normal_ticks + 1, thresholdTest.normal_ticks)
        print('Ticks needed: %d, currently %d ticks' % (thresholdTest.normal_ticks, i.normal_ticks))
        if (i.normal_ticks == thresholdTest.normal_ticks):
            if (i.pending_status != i.current_status):
                twerkIt = True
                i.current_status = i.pending_status
                i.closed_dttm = timezone.now()
                i.closed_sw = True
            i.current_status = IncidentStatusChoices.Normal
    i.save()

    if (twerkIt):
        # Create Issue Notification
        IncidentNotification(i.id)
