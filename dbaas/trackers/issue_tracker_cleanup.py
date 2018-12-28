import datetime

from django.utils import timezone

from dbaas.models import IssueTracker, IssueStatusChoices, IssueNotification, ApplicationContact



def IssueTrackerCleanup():
    headerColor = 'color:lightorange'
    issueTracker = IssueTracker.objects.filter(closed_sw=False, last_dttm__lte=timezone.now()-datetime.timedelta(days=1))
    for i in issueTracker:
        i.closed_sw = True
        lastDttm = i.last_dttm
        i.current_status = IssueStatusChoices.Unknown
        i.pending_status = IssueStatusChoices.Unknown
        i.save()
        print('Closing Issue: %d, No activity for the last day.  Assuming something has changed.', i.id)


        print('============================================')
        print('Create a new Issue Notification and TwerkIt!')
        mySubjectTemplate = '''<span style="%s">%s</span>: Server:%s,
                    %s: %s, 
                    No Activity
                    '''
        mySubject = mySubjectTemplate % (
            headerColor, 'Closing', i.server.server_name,
            i.checker_threshold.checker_base_element.metric_name, i.element_details,
            i.checker_threshold.checker_base_element.metric_element)
        myHtmlTemplate = '''<h1><span style="%s">%s</span> Server: %s</h1>\n
                    %s: %s on %s <br>\n
                    <br>\n
                    Closing due to no activity in the last day.  Something has changed.
                    <br>\n
                    Started Tracking: %s <br>\n
                    Last Activity: %s <br>\n
                    <br>\n
                    IssueTrackerId: %s <br>\n
                    <br>\n
                    Link to Issue: <a href="http://0.0.0.0:8000/clusters/%s/servers/%s/issuetrackers/%s">Click</a> <br>\n
                    '''
        myBody = myHtmlTemplate % (
            headerColor, 'Closing', i.server.server_name,
            i.checker_threshold.checker_base_element.metric_name, i.checker_threshold.checker_base_element.metric_element, i.element_details,
            timezone.datetime.strftime(i.start_dttm, "%a %b %d, %Y %H:%M"),
            timezone.datetime.strftime(lastDttm, "%a %b %d, %Y %H:%M"),
            i.id,
            i.server.cluster_id, i.server_id, i.id)

        i = IssueNotification(issue_tracker_id=i.id,
                              application=i.server.cluster.application,
                              notification_method='Twerking',
                              notification_subject=mySubject,
                              notification_body=myBody)
        i.save()


        print('Notify the following contacts')
        for ac in ApplicationContact.objects.filter(application=i.server.cluster.application, contact__active_sw=True):
            print('  %s: email: %s, phone: %s' % (
                ac.contact.contact_name,
                ac.contact.contact_email,
                ac.contact.contact_phone))
        print('============================================\n')

