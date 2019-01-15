from django.utils import timezone

from metrics.models import *


def GetMetricsCollectionErrors(s):
  print('\n[CollectionErrors]: ' + s.server_name )
  data = Metrics_Cpu.objects.filter(server_id=s.id).last()
  print('cpu')
  if (data.error_cnt > 5):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'CPU'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()

  print('cpuLoad')
  data = Metrics_CpuLoad.objects.filter(server_id=s.id).last()
  if (data.error_cnt > 5):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'CPU Load'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()

  print('MountPoint')
  data = Metrics_MountPoint.objects.filter(server_id=s.id).last()
  if (data.error_cnt > 3):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'Mount Points'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()

  print('HostDetail')
  data = Metrics_HostDetail.objects.filter(server_id=s.id).last()
  if (data.error_cnt > 5):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'HostDetail'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()

  print('PingDb')
  data = Metrics_PingDb.objects.filter(server_id=s.id).last()
  if (data.error_cnt > 5):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'Ping DB'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()

  print('PingServer')
  data = Metrics_PingServer.objects.filter(server_id=s.id).last()
  if (data.error_cnt > 5):
    metrics_CollectionError = Metrics_CollectionError()
    metrics_CollectionError.server = s
    metrics_CollectionError.metric_name = 'Ping Server'
    metrics_CollectionError.created_dttm = timezone.now()
    metrics_CollectionError.error_cnt = data.error_cnt
    metrics_CollectionError.error_msg = data.errorMsg
    metrics_CollectionError.save()