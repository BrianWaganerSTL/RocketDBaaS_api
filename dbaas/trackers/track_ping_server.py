import logging

from django.core.mail import EmailMessage
from django.utils import timezone

from dbaas.models import IssueNotification, Server, IssueTracker, IssueStatusChoices, ApplicationContact, CheckerThreshold, MetricsPingServer
from dbaas.trackers.send_notification_email import SendNotificationEmail
from dbaas.utils.DynCompare import DynCompare

mySubjectTemplate = '%s: Server: %s, %s: %s, Current Test: (%s)'
myHtmlTemplate = '''<h1 style="%s; margin:0px; padding:1rem">Server: %s &nbsp;&nbsp;&nbsp; <span style="text-decoration: underline">%s</span></h1>
    <br>\n
    %s: %s <br>\n
    <br>\n
    Current Value: %s<br>\n
    Current Test: (%s) <br>\n
    <br>\n
    Started Tracking: %s <br>\n
    Last Activity: %s <br>\n
    <br>\n
    Issue Tracker ID: %s <br>\n
    <br>\n
    Link to Issue: <a href="http://0.0.0.0:8000/clusters/%s/servers/%s/issuetrackers/%s">Click</a> <br>\n
    '''


def Track_PingServer(slimServer, metrics_ping_server_id):
    metricsPingServer = MetricsPingServer.objects.get(id=metrics_ping_server_id)

    try:
        chkrThreshold = CheckerThreshold.objects\
            .filter(active_sw=True,
                    checker_base_element__active_sw=True,
                    checker_base_element__metric_name='PingServer',
                    checker_base_element__metric_element='ping_server_ms',
                    server_override__isnull=True)[0]
    except:
        logging.error('Found no active Checker for Ping Server (ping_server_ms)')
        return
    else:
        ping_server_ms = metricsPingServer.ping_server_response_ms
        if DynCompare(ping_server_ms, chkrThreshold.critical_predicate_type, chkrThreshold.critical_value):
            thresholdLevel = IssueStatusChoices.Critical
            thresholdTestWithValues = '%d %s %s' % (ping_server_ms, chkrThreshold.critical_predicate_type, chkrThreshold.critical_value)
            print('%s Threshold' % thresholdLevel)
        elif DynCompare(ping_server_ms, chkrThreshold.warning_predicate_type, chkrThreshold.warning_value):
            thresholdLevel = IssueStatusChoices.Warning
            thresholdTestWithValues = '%d %s %s' % (ping_server_ms, chkrThreshold.warning_predicate_type, chkrThreshold.warning_value)
            print('%s Threshold' % thresholdLevel)
        else:
            thresholdLevel = IssueStatusChoices.Normal
            thresholdTestWithValues = '%d %s %s' % (ping_server_ms, chkrThreshold.normal_predicate_type, chkrThreshold.normal_value)
            print('Keep trying to being it down')


    #  Now Create a IssueTracker if one doesn't already exist
    twerkIt = False
    server = Server.objects.get(id=slimServer.id)
    try:
        issueTracker = IssueTracker.objects.filter(server_id=server.id, checker_threshold=chkrThreshold, closed_sw=False)[0]
    except:
        if (thresholdLevel in ['Critical','Warning']):
            issueTracker = IssueTracker(server_id=server.id,
                                        checker_threshold=chkrThreshold,
                                        pending_status=thresholdLevel)
            print('Created a IssueTracker')
        else:
            return

    t = issueTracker
    t.save()  # Save so I get the datetimes and other default
    if thresholdLevel == 'Critical':
        t.critical_ticks = min(t.critical_ticks + 1, chkrThreshold.critical_ticks)
        t.warning_ticks = min(t.warning_ticks + 1, chkrThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (chkrThreshold.critical_ticks, t.critical_ticks))
        if (t.critical_ticks == chkrThreshold.critical_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                headerColor = 'background-color:red'
            t.pending_status = IssueStatusChoices.Critical

    elif thresholdLevel == 'Warning':
        t.critical_ticks = max(t.critical_ticks - 1, 0)
        t.warning_ticks = min(t.warning_ticks + 1, chkrThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (chkrThreshold.warning_ticks, t.warning_ticks))
        if (t.warning_ticks == chkrThreshold.warning_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                headerColor = 'background-color:orange'
            t.current_status = IssueStatusChoices.Warning

    elif thresholdLevel == 'Normal':
        t.critical_ticks = max(t.critical_ticks - 1, 0)
        t.warning_ticks = max(t.warning_ticks - 1, 0)
        t.normal_ticks = min(t.normal_ticks + 1, chkrThreshold.normal_ticks)
        print('Ticks needed: %d, currently %d ticks' % (chkrThreshold.normal_ticks, t.normal_ticks))
        if (t.normal_ticks == chkrThreshold.normal_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                t.closed_sw = True
                headerColor = 'background-color:green'
                t.current_status = IssueStatusChoices.Normal
    t.save()


    # Now Create a Issue Notification
    if (twerkIt):
        print('============================================')
        print('Create a new Issue Notification and TwerkIt!')
        mySubject = mySubjectTemplate % (
            thresholdLevel, t.server.server_name,
            chkrThreshold.checker_base_element.metric_name,
            chkrThreshold.checker_base_element.metric_element,
            thresholdTestWithValues)
        myBody = myHtmlTemplate % (
            headerColor, t.server.server_name, thresholdLevel,
            chkrThreshold.checker_base_element.metric_name,
            chkrThreshold.checker_base_element.metric_element,
            metricsPingServer.ping_server_ms,
            thresholdTestWithValues,
            timezone.datetime.strftime(t.start_dttm, "%a %b %d, %Y %H:%M"),
            timezone.datetime.strftime(t.last_dttm, "%a %b %d, %Y %H:%M"),
            t.id,
            t.server.cluster_id, t.server_id, t.id)

        i = IssueNotification(issue_tracker_id=t.id,
                              application=t.server.cluster.application,
                              notification_method='Twerking',
                              notification_subject=mySubject,
                              notification_body=myBody)
        i.save()

        SendNotificationEmail(i.id)
