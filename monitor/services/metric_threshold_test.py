from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone

from dbaas.models import Server
from dbaas.utils.DynCompare import DynCompare
from monitor.models import ThresholdTest, Incident, IncidentDetail
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
    # print('returning')
    pass
    return

  # print('In MetricThresholdTest: category_name=' + category_name + ', metric_name=' + metric_name + ', metric_value=' + str(metric_value) + ', detail_element=' + detail_element)
  critical_value = eval(thresholdTest.critical_value.replace("<<CPU>>", str(server.cpu)))
  warning_value = eval(thresholdTest.warning_value.replace("<<CPU>>", str(server.cpu)))
  # print('warning_value: ' + str(warning_value) + ', critical_value: ' + str(critical_value))

  if DynCompare(metric_value, thresholdTest.critical_predicate_type, critical_value):
    pendingStatus = Incident.StatusChoices.CRITICAL
    # Looking to see if thresholdTest.critical_value has a << >> variable in it
    if (str(critical_value) == thresholdTest.critical_value):
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.critical_predicate_type, thresholdTest.critical_value)
    else:
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.critical_predicate_type, str(critical_value) + ' (' + thresholdTest.critical_value) + ')'

  elif DynCompare(metric_value, thresholdTest.warning_predicate_type, warning_value):
    pendingStatus = Incident.StatusChoices.WARNING
    if (str(warning_value) == thresholdTest.warning_value):
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, thresholdTest.warning_value)
    else:
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, str(warning_value) + ' (' + thresholdTest.warning_value) + ')'

  else:
    pendingStatus = Incident.StatusChoices.NORMAL
    if (str(warning_value) == thresholdTest.warning_value):
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, thresholdTest.warning_value)
    else:
      CurTestWithValues = '%d %s %s' % (metric_value, thresholdTest.warning_predicate_type, str(warning_value) + ' (' + thresholdTest.warning_value) + ')'

  print('Pending Status: %s' % pendingStatus)

  #  Now Create an Incident if one doesn't already exist
  twerkIt = False
  try:
    # print('Try to find a current incident')
    i = Incident.objects.filter(server_id=server.id, threshold_test=thresholdTest, closed_sw=False)[0]
    # print('Found a current incident id: ' + str(i.id))

    i.detail_element = detail_element
    i.cur_test_w_values = CurTestWithValues
    i.cur_value = metric_value
    i.max_value = max(i.max_value, metric_value)
    i.max_value = min(i.max_value, metric_value)
    i.last_dttm = timezone.now()
    i.save()
  except:
    # print('Did not find an existing Incident')
    if (pendingStatus != Incident.StatusChoices.CRITICAL and pendingStatus != Incident.StatusChoices.WARNING):
      # print('Nothing to do, Return')
      return
    else:
      # print('Create an Incident with server.id:' + str(server.id) + ',  pending_status:' + pendingStatus)
      try:
        i = Incident(server_id=server.id, threshold_test=thresholdTest, max_status=Incident.StatusChoices.WATCHING, current_status=Incident.StatusChoices.WATCHING,
                     pending_status=pendingStatus, min_value=metric_value, max_value=metric_value, detail_element=detail_element, cur_test_w_values=CurTestWithValues,
                     cur_value=metric_value, last_dttm=timezone.now())
        i.save()  # Save so I get the datetimes and other default
        print('Created a Incident')
        pass
      except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
        print('Error: ' + str(ex))
      except Exception as ex:
        print('Error: ' + str(ex))

  if (i.pending_status == Incident.StatusChoices.CRITICAL):
    i.critical_ticks = min(i.critical_ticks + 1, thresholdTest.critical_ticks)
    i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
    i.normal_ticks = max(i.normal_ticks - 1, 0)
    # print('Critical Ticks needed: %d, currently %d ticks' % (thresholdTest.critical_ticks, i.critical_ticks))
    # print('if (' + str(i.critical_ticks) + ' == ' + str(thresholdTest.critical_ticks) + ')')
    if (i.critical_ticks == thresholdTest.critical_ticks):
      if (i.current_status != i.pending_status):
        twerkIt = True
        i.current_status = i.pending_status
        i.max_status = i.pending_status
        # print('Set current_status = ' + i.pending_status)
      i.pending_status = Incident.StatusChoices.CRITICAL
      # print('Set pending_status = Critical')

  elif (i.pending_status == Incident.StatusChoices.WARNING):
    i.critical_ticks = max(i.critical_ticks - 1, 0)
    i.warning_ticks = min(i.warning_ticks + 1, thresholdTest.warning_ticks)
    i.normal_ticks = max(i.normal_ticks - 1, 0)
    # print('Warning Ticks needed: %d, currently %d ticks' % (thresholdTest.warning_ticks, i.warning_ticks))
    if (i.warning_ticks == thresholdTest.warning_ticks):
      if (i.current_status != i.pending_status):
        twerkIt = True
        i.current_status = i.pending_status
        if (i.max_status != Incident.StatusChoices.CRITICAL):
          i.max_status = i.pending_status
        # print('Set current_status = ' + i.pending_status)
      i.current_status = Incident.StatusChoices.WARNING

  elif (i.pending_status == Incident.StatusChoices.NORMAL):
    i.critical_ticks = max(i.critical_ticks - 1, 0)
    i.warning_ticks = max(i.warning_ticks - 1, 0)
    i.normal_ticks = min(i.normal_ticks + 1, thresholdTest.normal_ticks)
    # print('Normal Ticks needed: %d, currently %d ticks' % (thresholdTest.normal_ticks, i.normal_ticks))
    if (i.normal_ticks == thresholdTest.normal_ticks):
      if (i.current_status != i.pending_status):
        if (i.current_status == Incident.StatusChoices.WATCHING):
          # Never got out of Watchingmakemi, just delete it
          i.delete(keep_parents=True)
        else:
          twerkIt = True
          i.current_status = i.pending_status
          # print('Set current_status = ' + i.pending_status)
          if (i.max_status != Incident.StatusChoices.CRITICAL and i.max_status != Incident.StatusChoices.WARNING):
            i.max_status = i.pending_status
          i.closed_dttm = timezone.now()
          i.closed_sw = True
      i.current_status = Incident.StatusChoices.NORMAL
  i.save()

  incidentDetail = IncidentDetail(incident=i, cur_value=i.cur_value, min_value=i.min_value, max_value=i.max_value, cur_test_w_values=i.cur_test_w_values,
                                  pending_status=i.pending_status, max_status=i.max_status, current_status=i.current_status, critical_ticks=i.critical_ticks,
                                  warning_ticks=i.warning_ticks, normal_ticks=i.normal_ticks)
  incidentDetail.save()

  # print('Get Ready to...')
  print('\n' +
        '>>>  Should We TwerkIt Baby???' + str(twerkIt) + ' ' + i.server.server_name + ' ' +
        i.threshold_test.threshold_metric.category.category_name + ': ' +
        i.threshold_test.threshold_metric.metric_name + ' ' +
        str(i.threshold_test.detail_element) + ' ' +
        'Current [' + i.cur_test_w_values + ']\n' +
        '>>>  pending_status: ' + i.pending_status + ', current_status: ' + i.current_status + ' Ticks(N,W,C):(' + str(i.normal_ticks) + ',' + str(i.warning_ticks) + ',' + str(critical_value) + ')\n')
  print('>>>  Started: ' + str(i.start_dttm) + ', ID=' + str(i.id))
  if (twerkIt):
    # Create Issue Notification
    # print('SendIncidentNotification')
    SendIncidentNotification(i.id)
