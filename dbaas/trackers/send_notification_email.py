from django.core.mail import EmailMessage

from dbaas.models import IssueNotification, ApplicationContact


def SendNotificationEmail(IssueNotificationId):
    i = IssueNotification.object.get(IssueNotificationId)

    dbmsType = i.server.cluster.dbms_type
    if (dbmsType == 'PostgreSQL'):
        emailFrom = 'NextGenDBaaS<DBA-PostgreSQL@express-scripts.com>'
        emailCc = ['DBA - PostgreSQL <DBA-PostgreSQL@express-scripts.com>']
        replyTo = ['DBA - PostgreSQL <DBA-PostgreSQL@express-scripts.com>']
    elif (dbmsType == 'MongoDB'):
        emailFrom = 'NextGenDBaaS<DBA-MongoDB@express-scripts.com>>'
        emailCc = ['DBA - MongoDB <DBA-MongoDB@express-scripts.com>']
        replyTo = ['DBA - MongoDB <DBA-MongoDB@express-scripts.com>']

    # Send the Notification out to the following
    print('Notify the following contacts')
    for ac in ApplicationContact.objects.filter(application=t.server.cluster.application, contact__active_sw=True):
        print('  %s: email: %s, phone: %s' % (
            ac.contact.contact_name,
            ac.contact.contact_email,
            ac.contact.contact_phone))

        msg = EmailMessage(subject=i.notification_subject, body=i.notification_body, from_email=emailFrom, to=[ac.contact.contact_email], bcc=None,
                           connection=None, attachments=None, headers=None, cc=emailCc, reply_to=replyTo)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()

    print('============================================\n')
