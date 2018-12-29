from django.utils import timezone

from monitor.models import Incident, IssueStatusChoices
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
    Link to Issue: <a href="http://0.0.0.0:8000/clusters/%s/servers/%s/issuetrackers/%s">Click</a> <br>\n
    '''

def IncidentNotification(incidentId):
    i = Incident.objects.get(incidentId)

    print('============================================')
    print('Create a new Issue Notification and TwerkIt!')

    if (i.current_status == IssueStatusChoices.Critical):
        headerColor = 'background-color:red'
    elif (i.current_status == IssueStatusChoices.Warning):
        headerColor = 'background-color:orange'
    elif (i.current_status == IssueStatusChoices.Normal):
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

    note = IncidentNotification(incident=i,
                                application=i.server.cluster.application,
                                notification_method='Email',
                                notification_subject=mySubject,
                                notification_body=myBody)
    note.save()

    if (note.notification_method == 'Email'):
        SendNotificationEmail(note.id)