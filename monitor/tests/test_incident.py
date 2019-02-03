from django.test import TestCase
from django.utils import timezone

from dbaas.models import Server, DbmsTypeChoices
from metrics.models import Metrics_Cpu
from monitor.models import ThresholdTest, Incident, ThresholdNotificationMethodLookup, ThresholdCategoryLookup, ThresholdMetricLookup, PredicateTypeChoices, \
  IncidentNotification
from monitor.services.metric_threshold_test import MetricThresholdTest


class Test_MetricThreshold(TestCase):
  def testMetricThreshold_Normal_Warning_Warning(self):
    notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
    notifyMethod1.save()

    category1 = ThresholdCategoryLookup(category_name='Cpu')
    category1.save()

    thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
    thresholdMetric1.save()

    testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
                  normal_ticks=2,
                  warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
                  critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
                  notification_method=notifyMethod1,
                  active_sw=True, detail_element='')
    testCpu.save()

    server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
    server1.save()
    print(server1.node_role)
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()
    print(cpuNormal.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 1)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).count(), 0)

    # ===================================================================================
    #  Should create a pending WARNING
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()
    print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 2)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  Should create another WarningTick, thus making it a Warning (current and pending)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()
    print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 3)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().warning_ticks, 2)


  def testMetricThreshold_Critical_Normal_Normal_Deleted(self):
    notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
    notifyMethod1.save()

    category1 = ThresholdCategoryLookup(category_name='Cpu')
    category1.save()

    thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
    thresholdMetric1.save()

    testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
                            normal_ticks=2,
                            warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
                            critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
                            notification_method=notifyMethod1,
                            active_sw=True, detail_element='')
    testCpu.save()

    server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
    server1.save()
    print(server1.node_role)
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

    # ===================================================================================
    # Should create a pending Critical
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=4, created_dttm=timezone.now())
    cpuNormal.save()
    print(cpuNormal.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 1)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  Should create a pending Normal
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuWarning.save()
    print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 2)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    print(Incident.objects.filter(server=server1, threshold_test=testCpu).first())
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.NORMAL)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  Should create another NormalTick, thus making it a Normal (current and pending)
    #  Since it was never a Warning or Critical, it should be just deleted
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuWarning.save()
    print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 3)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).count(), 0)


  # def testMetricThreshold_Setup(self):
  #   notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
  #   notifyMethod1.save()
  #
  #   category1 = ThresholdCategoryLookup(category_name='Cpu')
  #   category1.save()
  #
  #   thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
  #   thresholdMetric1.save()
  #
  #   testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
  #                 normal_ticks=2,
  #                 warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
  #                 critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
  #                 notification_method=notifyMethod1,
  #                 active_sw=True, detail_element='')
  #   testCpu.save()
  #
  #   server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
  #   server1.save()
  #   print(server1.node_role)
  #   self.assertEquals(Server.objects.count(), 1)
  #   self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

  def testMetricThreshold_Normal_Warning_Warning_Email(self):
    notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
    notifyMethod1.save()

    category1 = ThresholdCategoryLookup(category_name='Cpu')
    category1.save()

    thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
    thresholdMetric1.save()

    testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
                            normal_ticks=2,
                            warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
                            critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
                            notification_method=notifyMethod1,
                            active_sw=True, detail_element='')
    testCpu.save()

    server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
    server1.save()
    print(server1.node_role)
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()
    print(cpuNormal.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 1)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).count(), 0)

    # ===================================================================================
    #  Should create a pending WARNING
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()
    print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 2)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  Should create another WarningTick, thus making it a Warning (current and pending)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()
    # print(cpuWarning.cpu_idle_pct)
    self.assertEquals(Metrics_Cpu.objects.count(), 3)

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    i = Incident.objects.filter(server=server1, threshold_test=testCpu).first()
    self.assertEquals(i.pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(i.current_status, Incident.StatusChoices.WARNING)
    self.assertEquals(i.warning_ticks, 2)

    iNote = IncidentNotification.objects.filter(incident=i)
    self.assertEquals(iNote.count(), 1)
    self.assertEquals(iNote.first().application, None)
    self.assertEquals(iNote.first().notification_method, i.threshold_test.notification_method)
    # print(iNote.first().notification_subject)
    # print(iNote.first().notification_body)


  def testMetricThreshold_Normal_Warning_Critical_Critical_Email(self):
    # ===================================================================================
    #  SetUp
    notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
    notifyMethod1.save()

    category1 = ThresholdCategoryLookup(category_name='Cpu')
    category1.save()

    thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
    thresholdMetric1.save()

    testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
                            normal_ticks=2,
                            warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
                            critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
                            notification_method=notifyMethod1,
                            active_sw=True, detail_element='')
    testCpu.save()

    server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
    server1.save()
    print(server1.node_role)
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()


    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).count(), 0)

    # ===================================================================================
    #  Should create a pending WARNING
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  CRITICAL with PENDING CRITICAL, and CURRENT WATCHING (Because since it's happening so fast just watch)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=4, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  CRITICAL with PENDING CRITICAL, and CURRENT CRITICAL (causing Notification)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=4, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    i = Incident.objects.filter(server=server1, threshold_test=testCpu).first()
    self.assertEquals(i.pending_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(i.current_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(i.warning_ticks, 2)

    # ===================================================================================
    #  Notification Created
    iNote = IncidentNotification.objects.filter(incident=i)
    self.assertEquals(iNote.count(), 1)
    self.assertEquals(iNote.first().application, None)
    self.assertEquals(iNote.first().notification_method, i.threshold_test.notification_method)
    # print(iNote.first().notification_subject)
    # print(iNote.first().notification_body)


  def testMetricThreshold_Normal_Warning_Critical_Critical_Email(self):
    # ===================================================================================
    #  SetUp
    notifyMethod1 = ThresholdNotificationMethodLookup(notification_method='Email')
    notifyMethod1.save()

    category1 = ThresholdCategoryLookup(category_name='Cpu')
    category1.save()

    thresholdMetric1 = ThresholdMetricLookup(category=category1, metric_name='cpu_idle_pct', detail_element_sw=False)
    thresholdMetric1.save()

    testCpu = ThresholdTest(threshold_metric=thresholdMetric1,
                            normal_ticks=2,
                            warning_ticks=2, warning_predicate_type=PredicateTypeChoices.LTH, warning_value=20,
                            critical_ticks=2, critical_predicate_type=PredicateTypeChoices.LTH, critical_value=5,
                            notification_method=notifyMethod1,
                            active_sw=True, detail_element='')
    testCpu.save()

    server1 = Server(server_name='ch5xx0001', node_role=Server.NodeRoleChoices.PRIMARY, dbms_type=DbmsTypeChoices.PostgreSQL)
    server1.save()
    print(server1.node_role)
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.filter(server_name='ch5xx0001').count(), 1)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()


    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).count(), 0)

    # ===================================================================================
    #  Should create a pending WARNING
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=15, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.WARNING)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  CRITICAL with PENDING CRITICAL, and CURRENT WATCHING (Because since it's happening so fast just watch)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=4, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().pending_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(Incident.objects.filter(server=server1, threshold_test=testCpu).first().current_status, Incident.StatusChoices.WATCHING)

    # ===================================================================================
    #  CRITICAL with PENDING CRITICAL, and CURRENT CRITICAL (causing Notification)
    cpuWarning = Metrics_Cpu(server=server1, cpu_idle_pct=4, created_dttm=timezone.now())
    cpuWarning.save()

    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuWarning.cpu_idle_pct, '')

    i = Incident.objects.filter(server=server1, threshold_test=testCpu).first()
    self.assertEquals(i.pending_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(i.current_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(i.warning_ticks, 2)

    # ===================================================================================
    #  Notification Created
    iNote = IncidentNotification.objects.filter(incident=i)
    self.assertEquals(iNote.count(), 1)
    self.assertEquals(iNote.first().application, None)
    self.assertEquals(iNote.first().notification_method, i.threshold_test.notification_method)
    # print(iNote.first().notification_subject)
    # print(iNote.first().notification_body)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()
    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    i = Incident.objects.filter(server=server1, threshold_test=testCpu).first()
    self.assertEquals(i.pending_status, Incident.StatusChoices.NORMAL)
    self.assertEquals(i.current_status, Incident.StatusChoices.CRITICAL)
    self.assertEquals(i.normal_ticks, 1)

    # ===================================================================================
    #  Should create a pending Normal
    cpuNormal = Metrics_Cpu(server=server1, cpu_idle_pct=90, created_dttm=timezone.now())
    cpuNormal.save()
    MetricThresholdTest(server1, 'Cpu', 'cpu_idle_pct', cpuNormal.cpu_idle_pct, '')
    i = Incident.objects.filter(server=server1, threshold_test=testCpu).first()
    self.assertEquals(i.pending_status, Incident.StatusChoices.NORMAL)
    self.assertEquals(i.current_status, Incident.StatusChoices.NORMAL)
    self.assertEquals(i.normal_ticks, 2)
