import logging

from django.utils import timezone

from dbaas.models import IssueNotification, Server, Metrics_MountPoint, IssueTracker, IssueStatusChoices, ApplicationContact, CheckerThreshold
from dbaas.utils.DynCompare import DynCompare

mySubjectTemplate = '''<span style="%s">%s</span>: Server:%s,
    %s: %s, 
    Current Test: %s (%s)
    '''
myHtmlTemplate = '''<h1><span style="%s">%s</span> Server: %s</h1>\n
    %s: %s <br>\n
    <br>\n
    Currently Value: %s %s<br>\n
    Current Test: (%s) <br>\n
    <br>\n
    Started Tracking: %s <br>\n
    Current DateTime: %s <br>\n
    <br>\n
    IssueTrackerId: %s <br>\n
    <br>\n
    Link to Issue: <a href="http://0.0.0.0:8000/clusters/%s/servers/%s/issuetrackers/%s">Click</a> <br>\n
    '''


class Tracker:
    def __init__(self, slimServer, metrics_MountPoint, checkerThreshold,
                 thresholdLevel, thresholdTestWithValues):

        self.server = Server.objects.get(id=slimServer.id)
        self.metricsMountPoint = metrics_MountPoint
        self.checkerThreshold = checkerThreshold
        self.thresholdLevel = thresholdLevel
        self.thresholdTestWithValues = thresholdTestWithValues





def Track_MountPoints(slimServer, metrics_MountPoint_id):
    metrics_MountPoint = Metrics_MountPoint.objects.get(id=metrics_MountPoint_id)

    try:
        chkrThreshold = CheckerThreshold.objects\
            .filter(active_sw=True,
                    checker_base_element__active_sw=True,
                    checker_base_element__metric_name='MountPoint',
                    checker_base_element__metric_element='used_pct',
                    server_override__isnull=True)[0]
    except:
        logging.error('Found no active Checker for MountPoint (used_pct)')
        pass
    else:
        usedPct = metrics_MountPoint.used_pct
        if DynCompare(usedPct, chkrThreshold.critical_predicate_type, chkrThreshold.critical_value):
            thresholdLevel = IssueStatusChoices.Critical
            thresholdTestWithValues = '%d %s %s' % (usedPct, chkrThreshold.critical_predicate_type, chkrThreshold.critical_value)
            print('%s Threshold' % thresholdLevel)
        elif DynCompare(usedPct, chkrThreshold.warning_predicate_type, chkrThreshold.warning_value):
            thresholdLevel = IssueStatusChoices.Warning
            thresholdTestWithValues = '%d %s %s' % (usedPct, chkrThreshold.warning_predicate_type, chkrThreshold.warning_value)
            print('%s Threshold' % thresholdLevel)
        else:
            thresholdLevel = IssueStatusChoices.Normal
            thresholdTestWithValues = '%d %s %s' % (usedPct, chkrThreshold.normal_predicate_type, chkrThreshold.normal_value)
            print('Keep trying to being it down')

        myTracker = Tracker(slimServer, metrics_MountPoint, chkrThreshold, thresholdLevel, thresholdTestWithValues)
        UpdIssueTracker(myTracker)


def UpdIssueTracker(myTracker):
    twerkIt = False
    try:
        issueTracker = IssueTracker.objects.filter(server_id=myTracker.server.id,
                                                   checker_threshold=myTracker.checkerThreshold,
                                                   closed_sw=False)[0]
    except:
        if (myTracker.thresholdLevel in ['Critical','Warning']):
            issueTracker = IssueTracker(server_id=myTracker.server.id,
                                        checker_threshold=myTracker.checkerThreshold,
                                        pending_status=myTracker.thresholdLevel)
            print('Created a IssueTracker')

    t = issueTracker
    t.save()  # Save so I get the datetimes and other default
    if myTracker.thresholdLevel == 'Critical':
        t.critical_ticks = min(t.critical_ticks + 1, myTracker.checkerThreshold.critical_ticks)
        t.warning_ticks = min(t.warning_ticks + 1, myTracker.checkerThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (myTracker.checkerThreshold.critical_ticks, t.critical_ticks))
        if (t.critical_ticks == myTracker.checkerThreshold.critical_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                headerColor = 'color:red'
            t.pending_status = IssueStatusChoices.Critical

    elif myTracker.thresholdLevel == 'Warning':
        t.critical_ticks = max(t.critical_ticks - 1, 0)
        t.warning_ticks = min(t.warning_ticks + 1, myTracker.checkerThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)
        print('Ticks needed: %d, currently %d ticks' % (myTracker.checkerThreshold.warning_ticks, t.warning_ticks))
        if (t.warning_ticks == myTracker.checkerThreshold.warning_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                headerColor = 'color:orange'
            t.current_status = IssueStatusChoices.Warning

    elif myTracker.thresholdLevel == 'Normal':
        t.critical_ticks = max(t.critical_ticks - 1, 0)
        t.warning_ticks = max(t.warning_ticks - 1, 0)
        t.normal_ticks = min(t.normal_ticks + 1, myTracker.checkerThreshold.normal_ticks)
        print('Ticks needed: %d, currently %d ticks' % (myTracker.checkerThreshold.normal_ticks, t.normal_ticks))
        if (t.normal_ticks == myTracker.checkerThreshold.normal_ticks):
            if (t.pending_status != t.current_status):
                twerkIt = True
                t.current_status = t.pending_status
                t.closed_sw = True
                headerColor = 'color:green'
                t.current_status = IssueStatusChoices.Normal
    t.save()
    print('mount_point: ' + myTracker.metricsMountPoint.mount_point)

    if (twerkIt):
        print('============================================')
        print('Create a new Issue Notification and TwerkIt!')
        mySubject = mySubjectTemplate % (
            headerColor, myTracker.thresholdLevel, t.server.server_name,
            myTracker.checkerThreshold.checker_base_element.metric_name,
            myTracker.metricsMountPoint.mount_point,
            myTracker.checkerThreshold.checker_base_element.metric_element,
            myTracker.thresholdTestWithValues)
        myBody = myHtmlTemplate % (
            headerColor, myTracker.thresholdLevel, t.server.server_name,
            myTracker.checkerThreshold.checker_base_element.metric_name,
            myTracker.metricsMountPoint.mount_point,
            myTracker.checkerThreshold.checker_base_element.metric_element,
            myTracker.metricsMountPoint.used_pct,
            myTracker.thresholdTestWithValues,
            timezone.datetime.strftime(t.start_dttm, "%a %b %d, %Y %H:%M"),
            timezone.datetime.strftime(t.last_dttm, "%a %b %d, %Y %H:%M"),
            t.id,
            t.server.cluster_id, t.server_id, t.id)
        print('mount_point: ' + myTracker.metricsMountPoint.mount_point)

        i = IssueNotification(issue_tracker_id=t.id,
                              application=t.server.cluster.application,
                              notification_method='Twerking',
                              notification_subject=mySubject,
                              notification_body=myBody)
        i.save()

        print('Notify the following contacts')
        for ac in ApplicationContact.objects.filter(application=t.server.cluster.application, contact__active_sw=True):
            print('  %s: email: %s, phone: %s' % (
                ac.contact.contact_name,
                ac.contact.contact_email,
                ac.contact.contact_phone))
        print('============================================\n')


