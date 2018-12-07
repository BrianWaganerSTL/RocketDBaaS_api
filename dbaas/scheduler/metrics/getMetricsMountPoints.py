# This calls out to the server to ask for the data, then pulls it back and saves it.
from datetime import datetime
import time
import os
import requests
import switch as switch
from rest_framework.generics import get_object_or_404

from dbaas.models import MetricsMountPoint, MetricThreshold, MetricNameChoices, MetricCheck, IssueTracker, IssueStatusChoices, IssueNotification, ApplicationContact, Contact
from dbaas.utils.DynCompare import DynCompare

errCnt = [0] * 1000
metrics_port = 8080
mySubjectTemplate = '''
    <span style="%s">%s</span>: Server:%s,
    %s: %s, 
    Current Test: %s (%s)
    '''
myHtmlTemplate = '''
    <h1><span style="%s">%s</span>: Server %s</h1>
    %s: %s
    Currently Value: %s
    Current Test: %s (%s)
    
    Started Tracking: %s
    Current DateTime: %s
    
    IssueTrackerId: %s
    
    Link to Issue: http://0.0.0.0:8000/clusters/:id/servers/:id/issuetrackers/:id
    
    <h3>Ticket: %s<h3>
    '''

class Tracker:
    def __init__(self, serverId, metricsMountPoint, metricThreshold,
                 thresholdLevel, thresholdTestWithValues, currentValue):
        self.serverId = serverId
        self.metricsMountPoint = MetricsMountPoint(metricsMountPoint)
        self.metricThreshold = MetricThreshold(metricThreshold)
        self.thresholdLevel = thresholdLevel
        self.thresholdTestWithValues = thresholdTestWithValues
        self.currentValue = currentValue


def UpdIssueTracker(myTracker):
    try:
        issueTracker = IssueTracker.objects.filter(server_id=myTracker.serverId, metric_threshold_id=myTracker.metricThreshold.id, closed_sw=False)[:1]
        print('found a issueTracker')
        print(str(issueTracker))

    except:
        if (myTracker.thresholdLevel in ['Critical','Warning']):
            issueTracker = IssueTracker(server=myTracker.serverId, metric_threshold_id=myTracker.metricThreshold.id)
            print('Created a IssueTracker')
        else:
            # Currently no IssueTracker so don't create one, just return
            return;
    for t in issueTracker:
        if myTracker.thresholdLevel == 'Critical':
            print(t.critical_ticks)
            print(myTracker.metricThreshold.critical_ticks)
            t.critical_ticks = max(t.critical_ticks + 1, myTracker.metricThreshold.critical_ticks)
            t.warning_ticks = min(t.warning_ticks + 1, myTracker.metricThreshold.warning_ticks)
            t.normal_ticks = max(t.normal_ticks - 1, 0)

            if (t.critical_ticks == myTracker.metricThreshold.critical_ticks):
                t.last_status = t.current_status
                t.current_status = IssueStatusChoices.Critical
                notify = IssueNotification(server=myTracker.serverId)
                mySubject = mySubjectTemplate % (
                    'color:red', myTracker.thresholdLevel, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
                myBody = myHtmlTemplate % (
                    'color:red', myTracker.metricThreshold, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.currentValue,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues,
                    t.start_dttm.strftime("%a %b %d, $Y %H:%M"),
                    t.last_dttmm.strftime("%a %b %d, $Y %H:%M"),
                    t.id,
                    t.server.cluster_id, t.server_id, t.id,
                    t.ticket)

        elif myTracker.thresholdLevel == 'Warning':
            t.critical_ticks = max(t.critical_ticks - 1, 0)
            t.warning_ticks = min(t.warning_ticks + 1, myTracker.metricThreshold.warning_ticks)
            t.normal_ticks = max(t.normal_ticks - 1, 0)

            if (t.clear_ticks == myTracker.metricThreshold.warning_ticks):
                t.last_status = t.current_status
                t.current_status = IssueStatusChoices.Warning
                notify = IssueNotification(server=myTracker.serverId)
                mySubject = mySubjectTemplate % (
                    'color:orange', myTracker.thresholdLevel, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
                myBody = myHtmlTemplate % (
                    'color:orange', myTracker.metricThreshold, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.currentValue,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues,
                    t.start_dttm.strftime("%a %b %d, $Y %H:%M"),
                    t.last_dttmm.strftime("%a %b %d, $Y %H:%M"),
                    t.id,
                    t.server.cluster_id, t.server_id, t.id,
                    t.ticket)

        elif myTracker.thresholdLevel == 'Normal':
            t.critical_ticks = max(t.critical_ticks - 1, 0)
            t.warning_ticks = max(t.warning_ticks - 1, 0)
            t.normal_ticks = min(t.normal_ticks + 1, myTracker.metricThreshold.normal_ticks)

            if (t.normal_ticks == myTracker.metricThreshold.normal_ticks):
                t.last_status = t.current_status
                t.current_status = IssueStatusChoices.Normal
                t.closed_sw = True

                notify = IssueNotification(server=myTracker.serverId)
                mySubject = mySubjectTemplate % (
                    'color:green', myTracker.thresholdLevel, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
                myBody = myHtmlTemplate % (
                    'color:green', myTracker.metricThreshold, t.server.server_name,
                    myTracker.metricThreshold.metric_check.metric_name, myTracker.metricThreshold.metric_check.metric_element,
                    myTracker.currentValue,
                    myTracker.metricsMountPoint, myTracker.thresholdTestWithValues,
                    t.start_dttm.strftime("%a %b %d, $Y %H:%M"),
                    t.last_dttmm.strftime("%a %b %d, $Y %H:%M"),
                    t.id,
                    t.server.cluster_id, t.server_id, t.id,
                    t.ticket)
        t.save()

        if (t.last_status != t.current_status):
            print('Notify somebody')
            ac = ApplicationContact.objects.filter(application_id=t.server.cluster.application_id)[:1]
            i = IssueNotification(issue_tracker_id=t.id,
                                  notification_subject=mySubject,
                                  notification_body=myBody,
                                  application_contact_id=ac.values('application'))
            i.save()

            for ac in ApplicationContact.objects.filter(application_id=t.server.cluster.application_id,
                                                        contact__active_sw=True):
                print('%s: email: %s, phone: %s') % (
                    ac.contact.contact_name,
                    ac.contact.contact_email,
                    ac.contact.contact_phone)



def EvalThresholds(inUsedPct, metricsMountPoint, inServerId):
    mt = MetricThreshold.objects\
        .filter(active_sw=True,
                metric_check__active_sw=True,
                metric_check__metric_name='MountPoint',
                metric_check__metric_element='used_pct',
                server_override__isnull=True)[:1]
    for i in mt:
        if DynCompare(inUsedPct, i.critical_predicate_type, i.critical_value):
            thresholdLevel = IssueStatusChoices.Critical
            thresholdTestWithValues = '%d %s %s' % (inUsedPct, i.critical_predicate_type, i.critical_value)
            print(thresholdTestWithValues)
            print('%s Threshold' % thresholdLevel)
        elif DynCompare(inUsedPct, i.warning_predicate_type, i.warning_value):
            thresholdLevel = IssueStatusChoices.Warning
            thresholdTestWithValues = '%d %s %s' % (inUsedPct, i.warning_predicate_type, i.warning_value)
            print(thresholdTestWithValues)
            print('%s Threshold' % thresholdLevel)
        else:
            thresholdLevel = IssueStatusChoices.Normal
            thresholdTestWithValues = '%d %s %s' % (inUsedPct, i.normal_predicate_type, i.normal_value)
            print('Keep trying to being it down')
        myTracker = Tracker(inServerId, metricsMountPoint, i, thresholdLevel, thresholdTestWithValues, inUsedPct)
        UpdIssueTracker(myTracker)


def GetMetricsMountPoints(s):
    metricsMountPoint = MetricsMountPoint()
    url = 'http://' + s.server_ip + ':' + str(metrics_port) + '/api/metrics/mountpoints'
    print('MountPoints: ServerNm: ' + s.server_name + ', url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        metricsMountPoint.server_id = s
        metricsMountPoint.created_dttm = metrics['created_dttm']
        metricsMountPoint.mount_point = metrics['mount_point']
        metricsMountPoint.allocated_gb = metrics['allocated_gb']
        metricsMountPoint.used_gb = metrics['used_gb']
        metricsMountPoint.used_pct = metrics['used_pct']
        metricsMountPoint.error_cnt = error_cnt
        metricsMountPoint.save()
    except requests.exceptions.Timeout:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Timeout'
        metricsMountPoint.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Bad URL'
        metricsMountPoint.save()
    except requests.exceptions.RequestException as e:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsMountPoint.save()
    except requests.exceptions.HTTPError as err:
        errCnt[s.id] = errCnt[s.id] + 1
        metricsMountPoint.server_id = s
        metricsMountPoint.error_cnt = errCnt[s.id]
        metricsMountPoint.error_msg = 'Other Error ' + err
        metricsMountPoint.save()

    EvalThresholds(metricsMountPoint.used_pct, metricsMountPoint.mount_point, s.id)