from django.core.exceptions import FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone

from metrics.models import Metrics_CollectionError, Metrics_Cpu, Metrics_CpuLoad, Metrics_MountPoint, Metrics_HostDetail, Metrics_PingDb, Metrics_PingServer


def GetMetricsCollectionErrors(s):
  print('\n[CollectionErrors]: ' + s.server_name )

  print('cpu')
  try:
    data = Metrics_Cpu.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 5):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'CPU'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')

  print('cpuLoad')
  try:
    data = Metrics_CpuLoad.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 3):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'CPU Load'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')

  print('MountPoint')
  try:
    data = Metrics_MountPoint.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 3):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'Mount Points'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')

  print('HostDetail')
  try:
    data = Metrics_HostDetail.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 5):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'HostDetail'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')

  print('PingDb')
  try:
    data = Metrics_PingDb.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 5):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'Ping DB'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')

  print('PingServer')
  try:
    data = Metrics_PingServer.objects.filter(server_id=s.id).last()
    if (data.error_cnt >= 5):
      metrics_CollectionError = Metrics_CollectionError()
      metrics_CollectionError.server = data.server
      metrics_CollectionError.metric_name = 'Ping Server'
      metrics_CollectionError.created_dttm = timezone.now()
      metrics_CollectionError.error_cnt = data.error_cnt
      metrics_CollectionError.error_msg = data.error_msg
      metrics_CollectionError.save()
  except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
    print('Error: Saving a Metrics_CollectionError' + str(ex))
  except:
    print('ERROR: Saving it to the Metrics_CollectionError table')
