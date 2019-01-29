from django.core.exceptions import FieldDoesNotExist, FieldError
from django.core.mail import EmailMessage
from django.db import IntegrityError

from dbaas.models import ApplicationContact
from monitor.models import IncidentNotification


def SendNotificationEmail(IncidentNotificationId, dbmsType):
  print('In SendNotificationEmail')
  try:
    print('Try to find a current incident')
    notification = IncidentNotification.objects.filter(id=IncidentNotificationId)[0]
    print('Found a current IncidentNotification id: ' + str(notification.id))
  except:
    print('Did not find an existing IncidentNotification')

  print('dbmsType=' + dbmsType)
  if (dbmsType == 'PostgreSQL'):
    emailFrom = 'bwaganer<bwaganer@express-scripts.com>'
    emailCc = ['bwaganer<bwaganer@express-scripts.com>', ]
    replyTo = ['bwaganer<bwaganer@express-scripts.com>', ]
    # emailFrom = 'NextGenDBaaS<DBA-PostgreSQL@express-scripts.com>'
    # emailCc = ['DBA - PostgreSQL <DBA-PostgreSQL@express-scripts.com>']
    # replyTo = ['DBA - PostgreSQL <DBA-PostgreSQL@express-scripts.com>']
  elif (dbmsType == 'MongoDB'):
    emailFrom = 'NextGenDBaaS<DBA-MongoDB@express-scripts.com>'
    emailCc = ['DBA - MongoDB <DBA-MongoDB@express-scripts.com>', ]
    replyTo = ['DBA - MongoDB <DBA-MongoDB@express-scripts.com>', ]

  # Send the Notification out to the following
  print('Notify the following contacts')

  try:
    print('Try to find Application Contacts')
    applicationContacts = ApplicationContact.objects.filter(application=notification.application.id, contact__active_sw=True).all()
    print('Found it')
  except:
    print('Did not find an application Contacts')

  print('applicationContacts.count()=' + str(applicationContacts.count()))
  if (applicationContacts.count() == 0):
    try:
      print('No Application Contacts registered for this metric, just send to the CC list')
      msg = EmailMessage(subject=notification.notification_subject, body=notification.notification_body,
                         from_email=emailFrom, to=emailCc, bcc=None,
                         connection=None, attachments=None, headers=None, cc=None, reply_to=replyTo)
      msg.content_subtype = "html"  # Main content is now text/html
      msg.send()
    except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
      print('Error: ' + str(ex))
    except Exception as ex:
      print('Error: ' + str(ex))
      notification.error_msg = str(ex)[:2000]
      notification.save()
  else:
    print('Before loop to get contacts and send an email')
    for ac in applicationContacts:
      print('  %s: email: %s, phone: %s' % (
        ac.contact.contact_name,
        ac.contact.contact_email,
        ac.contact.contact_phone))

      try:
        msg = EmailMessage(subject=notification.notification_subject, body=notification.notification_body,
                           from_email=emailFrom, to=[ac.contact.contact_email], bcc=None,
                           connection=None, attachments=None, headers=None, cc=emailCc, reply_to=replyTo)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
      except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
        print('Error: ' + str(ex))
      except Exception as ex:
        print('Error: ' + str(ex))
        notification.error_msg = str(ex)[:2000]
        notification.save()

  print('===================  EMAIL SENT  =========================\n')
