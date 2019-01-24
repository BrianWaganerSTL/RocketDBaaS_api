from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone

from dbaas.models import Server
from dbaas.utils.DynCompare import DynCompare
from monitor.models import ThresholdTest, IncidentStatusChoices, Incident
from monitor.services.send_incident_notification import SendIncidentNotification


def MetricThresholdTest(slimServer, category_name, metric_name, metric_value, detail_element):
  # print('In MetricThresholdTest: category_name=' + category_name + ', metric_name=' + metric_name + ', metric_value=' + str(metric_value) + ', detail_element=' + detail_element)
  server = Server.objects.get(id=slimServer.id)
  try:
    thresholdTest = ThresholdTest.objects \
                      .filter(Q(active_sw=True) &
                              Q(threshold_metric__category__category_name=category_name) &
                              Q(threshold_metric__metric_name=metric_name) &
                              (Q(detail_element=detail_element) |
                               Q(threshold_metric__detail_element_sw=False)))[0]
    # print('Found an active ThresholdTest for ' + category_name + ' (' + metric_name + ') ' + detail_element)
  except:
    # print('Found no active ThresholdTest for ' + category_name + ' (' + metric_name + ') ' + detail_element)
    print('returning')
    pass
    return
  else:
    print('In MetricThresholdTest: category_name=' + category_name + ', metric_name=' + metric_name + ', metric_value=' + str(metric_value) + ', detail_element=' + detail_element)
    critical_value = eval(thresholdTest.critical_value.replace("<<CPU>>", str(server.cpu)))
    warning_value = eval(thresholdTest.warning_value.replace("<<CPU>>", str(server.cpu)))
    print('warning_value: ' + str(warning_value) + ', critical_value: ' + str(critical_value));
    if DynCompare(metric_value, thresholdTest.critical_predicate_type, critical_value):
      pendingThresholdLevel = IncidentStatusChoices.Critical
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.critical_predicate_type, thresholdTest.critical_value)
    elif DynCompare(metric_value, thresholdTest.warning_predicate_type, warning_value):
      pendingThresholdLevel = IncidentStatusChoices.Warning
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, thresholdTest.warning_value)
    else:
      pendingThresholdLevel = IncidentStatusChoices.Normal
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, thresholdTest.warning_value)

    print('Pending Threshold: %s' % pendingThresholdLevel)

  #  Now Create an Incident if one doesn't already exist
  twerkIt = False
  try:
    print('Try to find a current incident')
    i = Incident.objects.filter(server_id=server.id, threshold_test=thresholdTest, closed_sw=False)[0]
    print('Found a current incident id: ' + str(i.id))
  except:
    print('Did not find an existing Incident')
    print('pendingThresholdLevel=' + pendingThresholdLevel)
    if (pendingThresholdLevel == 'Critical' or pendingThresholdLevel == 'Warning'):
      print('Flag1')
      print('Create an Incident with server.id:' + str(server.id) + ',  pending_status:' + pendingThresholdLevel)
      try:
        i = Incident(server_id=server.id, threshold_test=thresholdTest, pending_status=pendingThresholdLevel, min_value=metric_value, max_value=metric_value)
      except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
        print('Error: ' + str(ex))
      except:
        print('Other error')
      print('Created a Incident')
    else:
      print('Nothing to do, Return')
      return

  print('Before setting incident fields')
  i.detail_element = detail_element
  i.cur_test_w_values = CurTestWithValues
  i.cur_value = metric_value

  if (metric_value > i.max_value):
    i.max_value = metric_value
  if (metric_value < i.min_value):
    i.min_value = metric_value

  i.last_dttm = timezone.now()
  print('Before saving incident fields')
  i.save()  # Save so I get the datetimes and other default

  if pendingThresholdLevel == 'Critical':
    i.critical_ticks = min(i.critical_ticks + 1, thresholdTest.critical_ticks)
    i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
    i.normal_ticks = max(i.normal_ticks - 1, 0)
    print('Critical Ticks needed: %d, currently %d ticks' % (thresholdTest.critical_ticks, i.critical_ticks))
    print('if (' + str(i.critical_ticks) + ' == ' + str(thresholdTest.critical_ticks) + ')')
    if (i.critical_ticks == thresholdTest.critical_ticks):
      if (i.pending_status != i.current_status):
        twerkIt = True
        i.current_status = i.pending_status
        print('Set current_status = ' + i.pending_status)
      i.pending_status = IncidentStatusChoices.Critical
      print('Set pending_status = Critical')

  elif pendingThresholdLevel == 'Warning':
    i.critical_ticks = max(i.critical_ticks - 1, 0)
    i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
    i.normal_ticks = max(i.normal_ticks - 1, 0)
    print('Warning Ticks needed: %d, currently %d ticks' % (thresholdTest.warning_ticks, i.warning_ticks))
    if (i.warning_ticks == thresholdTest.warning_ticks):
      if (i.pending_status != i.current_status):
        twerkIt = True
        i.current_status = i.pending_status
      i.current_status = IncidentStatusChoices.Warning

  elif pendingThresholdLevel == 'Normal':
    i.critical_ticks = max(i.critical_ticks - 1, 0)
    i.warning_ticks = max(i.warning_ticks - 1, 0)
    i.normal_ticks = min(i.normal_ticks + 1, thresholdTest.normal_ticks)
    print('Normal Ticks needed: %d, currently %d ticks' % (thresholdTest.normal_ticks, i.normal_ticks))
    if (i.normal_ticks == thresholdTest.normal_ticks):
      if (i.pending_status != i.current_status):
        twerkIt = True
        i.current_status = i.pending_status
        i.closed_dttm = timezone.now()
        i.closed_sw = True
      i.current_status = IncidentStatusChoices.Normal
  i.save()

  print('Get Ready to...')
  print('\n' +
        '>>>  Should We TwerkIt Baby???' + str(twerkIt) + ' ' + i.server.server_name + ' ' +
        i.threshold_test.threshold_metric.category.category_name + ': ' +
        i.threshold_test.threshold_metric.metric_name + ' ' +
        str(i.threshold_test.detail_element) + ' ' +
        'Current [' + i.cur_test_w_values + ']\n' +
        '>>>  PendingStatus: ' + i.pending_status + ', CurrentStatus: ' + i.current_status + ' Ticks(N,W,C):(' + str(i.normal_ticks) + ',' + str(i.warning_ticks) + ',' + str(critical_value) + ')\n')
  print('>>>  Started: ' + str(i.start_dttm) + ', ID=' + str(i.id))
  if (twerkIt):
    # Create Issue Notification
    print('SendIncidentNotification')
    SendIncidentNotification(i.id)
