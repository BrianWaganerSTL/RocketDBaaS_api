from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone

from monitor.models import Incident, IncidentStatusChoices, IncidentNotification, ThresholdNotificationMethodLookup
from monitor.services.send_notification_email import SendNotificationEmail

mySubjectTemplate = '%s: Server: %s, %s: %s, Current Test: %s (%s)'
myHtmlTemplate = '''<h1 style="%s; margin:0px; padding:1rem">Server: %s &nbsp;&nbsp;&nbsp; <span style="text-decoration: underline">%s</span></h1>
    <br>\n
    %s: %s <br>\n
    <br>\n
    Current Value: %s %s<br>\n
    Current Test: (%s) <br>\n
    <br>\n
    Started Tracking: %s <br>\n
    Last Activity: %s <br>\n
    <br>\n
    Issue Tracker ID: %s <br>\n
    <br>\n
    Link to Issue: <a href="http://0.0.0.0:8080/clusters/%s/servers/%s/incidents/%s">Click</a> <br>\n
    '''

def SendIncidentNotification(incidentId):
    print('============================================')
    try:
        print('Try to find a current incident')
        i = Incident.objects.filter(id=incidentId)[0]
        print('Found a current incident id: ' + str(i.id))
    except:
        print('Did not find an existing Incident')

    print('Create a new Issue Notification and TwerkIt!')

    if (i.current_status == IncidentStatusChoices.Critical):
        headerColor = 'background-color:red'
    elif (i.current_status == IncidentStatusChoices.Warning):
        headerColor = 'background-color:orange'
    elif (i.current_status == IncidentStatusChoices.Normal):
        headerColor = 'background-color:green'

    mySubject = mySubjectTemplate % (
        i.current_status, i.server.server_name,
        i.threshold_test.threshold_metric.metric_name,
        i.threshold_test.detail_element,
        i.detail_element, i.cur_test_w_values)
    myBody = myHtmlTemplate % (
        headerColor, i.server.server_name, i.current_status,
        i.threshold_test.threshold_metric.metric_name,
        i.detail_element, i.threshold_test.detail_element,
        i.cur_value,
        i.cur_test_w_values,
        timezone.datetime.strftime(i.start_dttm, "%a %b %d, %Y %H:%M"),
        timezone.datetime.strftime(i.last_dttm, "%a %b %d, %Y %H:%M"),
        i.id,
        i.server.cluster_id, i.server_id, i.id)

    try:
        print('NotificationMethod: ' + i.threshold_test.notification_method.notification_method)
        incidentNotification = IncidentNotification(incident_id=i.id,
                                                    application=i.server.cluster.application,
                                                    notification_method=i.threshold_test.notification_method,
                                                    notification_subject=mySubject,
                                                    notification_body=myBody)
        incidentNotification.save()
    except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
        print('Error: ' + str(ex))
    except:
        print('Other error')

    print('incidentNotification.notification_method.notification_method(' + incidentNotification.notification_method.notification_method+ ') == Email')
    if (incidentNotification.notification_method.notification_method == 'Email'):
        SendNotificationEmail(incidentNotification.id, i.server.dbms_type)
