# This calls out to the server to ask for the data, then pulls it back and saves it.
from datetime import datetime
import time
import os
import requests
import switch as switch
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from dbaas.models import MetricsMountPoint, CheckerThreshold, MetricNameChoices, CheckerBaseElement, IssueTracker, IssueStatusChoices, IssueNotification, ApplicationContact, Contact, \
    Server, Application
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
    def __init__(self, serverId, metricsMountPoint, checkerThreshold,
                 thresholdLevel, thresholdTestWithValues, currentValue):
        self.serverId = serverId
        self.metricsMountPoint = MetricsMountPoint(metricsMountPoint)
        self.checkerThreshold = checkerThreshold
        self.thresholdLevel = thresholdLevel
        self.thresholdTestWithValues = thresholdTestWithValues
        self.currentValue = currentValue


def UpdIssueTracker(myTracker):
    twerkIt = False
    issueTracker = IssueTracker.objects.filter(server_id=myTracker.serverId,
                                               metric_threshold_id=myTracker.checkerThreshold.id,
                                               closed_sw=False)[0]
    if (issueTracker):
        print('found a issueTracker')
    else:
        if (myTracker.thresholdLevel in ['Critical','Warning']):
            issueTracker = IssueTracker(server=myTracker.serverId, metric_threshold_id=myTracker.checkerThreshold.id)
            print('Created a IssueTracker')

    t = issueTracker
    t.save()  # Save so I get the datetimes and other default
    print('Inside forloop for issueTracker')
    if myTracker.thresholdLevel == 'Critical':
        print('Ticks needed: %d, currently %d ticks' % (myTracker.checkerThreshold.critical_ticks, t.critical_ticks))
        t.critical_ticks = min(t.critical_ticks + 1, myTracker.checkerThreshold.critical_ticks)
        t.warning_ticks = min(t.warning_ticks + 1, myTracker.checkerThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)

        if (t.critical_ticks == myTracker.checkerThreshold.critical_ticks):
            twerkIt = True
            t.prior_status = t.current_status
            t.current_status = IssueStatusChoices.Critical
            print('metric_name:' + myTracker.checkerThreshold.metric_check.metric_name)
            mySubject = mySubjectTemplate % (
                'color:red', myTracker.thresholdLevel, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name,
                myTracker.checkerThreshold.metric_check.metric_element,
                myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
            myBody = myHtmlTemplate % (
                'color:red', myTracker.checkerThreshold, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name, myTracker.checkerThreshold.metric_check.metric_element,
                myTracker.currentValue,
                myTracker.metricsMountPoint, myTracker.thresholdTestWithValues,
                timezone.datetime.strftime(t.start_dttm, "%a %b %d, %Y %H:%M"),
                timezone.datetime.strftime(t.last_dttm, "%a %b %d, %Y %H:%M"),
                t.id,
                t.server.cluster_id, t.server_id, t.id,
                t.ticket)

    elif myTracker.thresholdLevel == 'Warning':
        t.critical_ticks = max(t.critical_ticks - 1, 0)
        t.warning_ticks = min(t.warning_ticks + 1, myTracker.checkerThreshold.warning_ticks)
        t.normal_ticks = max(t.normal_ticks - 1, 0)

        if (t.clear_ticks == myTracker.checkerThreshold.warning_ticks):
            twerkIt = True
            t.prior_status = t.current_status
            t.current_status = IssueStatusChoices.Warning
            notify = IssueNotification(server=myTracker.serverId)
            mySubject = mySubjectTemplate % (
                'color:orange', myTracker.thresholdLevel, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name, myTracker.checkerThreshold.metric_check.metric_element,
                myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
            myBody = myHtmlTemplate % (
                'color:orange', myTracker.checkerThreshold, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name, myTracker.checkerThreshold.metric_check.metric_element,
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
        t.normal_ticks = min(t.normal_ticks + 1, myTracker.checkerThreshold.normal_ticks)

        if (t.normal_ticks == myTracker.checkerThreshold.normal_ticks):
            twerkIt = True
            t.prior_status = t.current_status
            t.current_status = IssueStatusChoices.Normal
            t.closed_sw = True

            notify = IssueNotification(server=myTracker.serverId)
            mySubject = mySubjectTemplate % (
                'color:green', myTracker.thresholdLevel, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name, myTracker.checkerThreshold.metric_check.metric_element,
                myTracker.metricsMountPoint, myTracker.thresholdTestWithValues)
            myBody = myHtmlTemplate % (
                'color:green', myTracker.checkerThreshold, t.server.server_name,
                myTracker.checkerThreshold.metric_check.metric_name, myTracker.checkerThreshold.metric_check.metric_element,
                myTracker.currentValue,
                myTracker.metricsMountPoint, myTracker.thresholdTestWithValues,
                t.start_dttm.strftime("%a %b %d, $Y %H:%M"),
                t.last_dttmm.strftime("%a %b %d, $Y %H:%M"),
                t.id,
                t.server.cluster_id, t.server_id, t.id,
                t.ticket)
    t.save()

    if (twerkIt):
        print('Notify somebody')
        ac = Application.objects.get(t.server.cluster.application_id)
        i = IssueNotification(issue_tracker_id=t.id,
                              notification_subject=mySubject,
                              notification_body=myBody,
                              application=ac)
        i.save()

        for ac in ApplicationContact.objects.filter(application=ac, contact__active_sw=True):
            print('%s: email: %s, phone: %s') % (
                ac.contact.contact_name,
                ac.contact.contact_email,
                ac.contact.contact_phone)



def EvalThresholds(inUsedPct, metricsMountPoint, inServerId):
    mt = CheckerThreshold.objects\
        .filter(active_sw=True,
                metric_check__active_sw=True,
                metric_check__metric_name='MountPoint',
                metric_check__metric_element='used_pct',
                server_override__isnull=True)[0]

    if DynCompare(inUsedPct, mt.critical_predicate_type, mt.critical_value):
        thresholdLevel = IssueStatusChoices.Critical
        thresholdTestWithValues = '%d %s %s' % (inUsedPct, mt.critical_predicate_type, mt.critical_value)
        print(thresholdTestWithValues)
        print('%s Threshold' % thresholdLevel)
    elif DynCompare(inUsedPct, mt.warning_predicate_type, mt.warning_value):
        thresholdLevel = IssueStatusChoices.Warning
        thresholdTestWithValues = '%d %s %s' % (inUsedPct, mt.warning_predicate_type, mt.warning_value)
        print(thresholdTestWithValues)
        print('%s Threshold' % thresholdLevel)
    else:
        thresholdLevel = IssueStatusChoices.Normal
        thresholdTestWithValues = '%d %s %s' % (inUsedPct, mt.normal_predicate_type, mt.normal_value)
        print('Keep trying to being it down')
    myTracker = Tracker(inServerId, metricsMountPoint, mt, thresholdLevel, thresholdTestWithValues, inUsedPct)
    UpdIssueTracker(myTracker)


def GetMetricsMountPoints(server):
    print('server='+str(server)+', id='+str(server.id) + ', ip=' + str(server.server_ip))
    metricsMountPoint = MetricsMountPoint()
    url = 'http://' + server.server_ip + ':' + str(metrics_port) + '/api/metrics/mountpoints'
    print('Check: MountPoints, ServerNm: ' + server.server_name + ', url=' + url)
    try:
        r = requests.get(url)
        metrics = r.json()
        print(metrics)

        error_cnt = 0
        metricsMountPoint.server = server
        metricsMountPoint.created_dttm = metrics['created_dttm']
        metricsMountPoint.mount_point = metrics['mount_point']
        metricsMountPoint.allocated_gb = metrics['allocated_gb']
        metricsMountPoint.used_gb = metrics['used_gb']
        metricsMountPoint.used_pct = metrics['used_pct']
        metricsMountPoint.error_cnt = error_cnt
        metricsMountPoint.save()
    except requests.exceptions.Timeout:
        errCnt[server.id] = errCnt[server.id] + 1
        metricsMountPoint.server = server
        metricsMountPoint.error_cnt = errCnt[server.id]
        metricsMountPoint.error_msg = 'Timeout'
        metricsMountPoint.save()
    except requests.exceptions.TooManyRedirects:
        errCnt[server.id] = errCnt[server.id] + 1
        metricsMountPoint.server = server
        metricsMountPoint.error_cnt = errCnt[server.id]
        metricsMountPoint.error_msg = 'Bad URL'
        metricsMountPoint.save()
    except requests.exceptions.RequestException as e:
        errCnt[server.id] = errCnt[server.id] + 1
        metricsMountPoint.server = server
        metricsMountPoint.error_cnt = errCnt[server.id]
        metricsMountPoint.error_msg = 'Catastrophic error. Bail ' + str(e)
        metricsMountPoint.save()
    except requests.exceptions.HTTPError as err:
        errCnt[server.id] = errCnt[server.id] + 1
        metricsMountPoint.server = server
        metricsMountPoint.error_cnt = errCnt[server.id]
        metricsMountPoint.error_msg = 'Other Error ' + err
        metricsMountPoint.save()

    EvalThresholds(metricsMountPoint.used_pct, metricsMountPoint.mount_point, server)