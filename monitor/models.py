from django.db import models
from django.db.models import ForeignKey, IntegerField, CASCADE, deletion, BooleanField, CharField, DateTimeField, DecimalField
from djchoices import DjangoChoices, ChoiceItem
from rest_framework.compat import MinValueValidator, MaxValueValidator

from dbaas.models import Server, INFINITY, Application

#
# class MetricNameChoices(DjangoChoices):
#     Cpu = ChoiceItem("CPU","CPU",1)
#     Load = ChoiceItem("Load","Load",2)
#     MountPoint = ChoiceItem("MountPoint","Mount Point",3)
#     PingDb = ChoiceItem("PingDB", "Ping DB", 4)
#     PingServer = ChoiceItem("PingServer", "Ping Server", 5)

class MetricThresholdPredicateTypeChoices(DjangoChoices):
    GTE = ChoiceItem(">=",">=",1)
    GTH = ChoiceItem(">",">",2)
    EQ = ChoiceItem("==","==",3)
    NE = ChoiceItem("!=","!=",4)
    LTE = ChoiceItem("<=", "<=", 5)
    LTH = ChoiceItem("<", "<", 6)

class IssueStatusChoices(DjangoChoices):
    Normal = ChoiceItem("Normal","Normal",1)
    Warning = ChoiceItem("Warning",'Warning',2)
    Critical = ChoiceItem("Critical","Critical",3)
    Blackout = ChoiceItem("Blackout","Blackout",4)
    Unknown = ChoiceItem("Unknown","Unknown", 6)


# ========================================================================




class ThresholdNotificationMethodLookup(models.Model):
    class Meta:
        db_table = 'monitor_threshold_notification_method_lookup'

    notification_method = CharField(max_length=15, null=False, default='')
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)
    active_sw = BooleanField(default=True, null=False)

class ThresholdCategoryLookup(models.Model):
    class Meta:
        db_table = 'monitor_threshold_category_lookup'

    category_name = CharField(max_length=15, null=False, default='')
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

class ThresholdMetricLookup(models.Model):
    class Meta:
        db_table = 'monitor_threshold_metric_lookup'

    category = ForeignKey(ThresholdCategoryLookup, on_delete=CASCADE, default='')
    metric_name = CharField(max_length=15, null=False, default='')
    detail_element_sw = BooleanField(default=False, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

class ThresholdTest(models.Model):
    class Meta:
        db_table = 'monitor_threshold_test'

    threshold_metric = ForeignKey(ThresholdMetricLookup, on_delete=CASCADE, default='')
    detail_element = CharField(max_length=50, null=False, default='')
    normal_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
    warning_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
    warning_predicate_type = CharField(max_length=15, null=False, default='>=', choices=MetricThresholdPredicateTypeChoices.choices)
    warning_value = CharField(max_length=100, null=False, default='')
    critical_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
    critical_predicate_type = CharField(max_length=15, null=False, default='>=', choices=MetricThresholdPredicateTypeChoices.choices)
    critical_value = CharField(max_length=100, null=False, default='')
    notification_method = ForeignKey(ThresholdNotificationMethodLookup, on_delete=CASCADE, default='')
    active_sw = BooleanField(default=True, null=False)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

class Incident(models.Model):
    class Meta:
        db_table = 'monitor_incident'
        ordering = ['-start_dttm']

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    threshold_test = ForeignKey(ThresholdTest, on_delete=deletion.ProtectedError, null=False, default='')
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    last_dttm = DateTimeField()
    closed_dttm = DateTimeField()
    closed_sw = BooleanField(default=False)
    min_value = DecimalField(null=False, default=0),
    cur_value = DecimalField(null=False, default=0),
    max_value = DecimalField(null=False, default=0),
    cur_test_w_values = CharField(max_length=500, null=False, default='')
    pending_status = CharField(max_length=15, null=False, default='', choices=IssueStatusChoices.choices)
    current_status = CharField(max_length=15, null=False, default='', choices=IssueStatusChoices.choices)
    detail_element = CharField(max_length=25, null=False, default='')
    critical_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
    warning_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
    normal_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
    note = CharField(max_length=4000, null=True, default='')
    note_by = CharField(max_length=30, null=True, default='')
    ticket = CharField(max_length=30, null=True, default='')
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class IncidentNotification(models.Model):
    class Meta:
        db_table = 'monitor_incident_notification'

    incident = ForeignKey(Incident, on_delete=deletion.CASCADE, null=True)
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=True)
    notification_dttm = DateTimeField(editable=False, auto_now_add=True)
    notification_method = ForeignKey(ThresholdNotificationMethodLookup, on_delete=CASCADE, default='')
    notification_subject = CharField(max_length=2000, null=False, default='')
    notification_body = CharField(max_length=10000, null=False, default='')
    acknowledged_by = CharField(max_length=30, null=False, default='')
    acknowledged_dttm = DateTimeField(null=False, default=INFINITY)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)






#
# class CheckerBaseElement(models.Model):
#     class Meta:
#         db_table = 'checker_base_element'
#
#     def __str__(self):
#         return self.metric_name + ' (' + self.metric_element + ')'
#
#     metric_name = CharField(max_length=15, null=False, default='', choices=MetricNameChoices.choices)
#     metric_element = CharField(max_length=50, null=False, default='')
#     created_dttm = DateTimeField(editable=False, auto_now_add=True)
#     updated_dttm = DateTimeField(auto_now=True)
#     active_sw = BooleanField(default=True, null=False)
#
#
# class CheckerThreshold(models.Model):
#     class Meta:
#         db_table = 'checker_threshold'
#
#     def __str__(self):
#         return self.checker_base_element
#
#     checker_base_element = ForeignKey(CheckerBaseElement, on_delete=CASCADE, default='')
#     server_override = ForeignKey(Server, on_delete=CASCADE, null=True, blank=True)
#     normal_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
#     normal_predicate_type = CharField(max_length=15, null=False, default='<', choices=MetricThresholdPredicateTypeChoices.choices)
#     normal_value = CharField(max_length=200, null=False, default='')
#     warning_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
#     warning_predicate_type = CharField(max_length=15, null=False, default='>=', choices=MetricThresholdPredicateTypeChoices.choices)
#     warning_value = CharField(max_length=200, null=False, default='')
#     critical_ticks = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, default=3)
#     critical_predicate_type = CharField(max_length=15, null=False, default='>=', choices=MetricThresholdPredicateTypeChoices.choices)
#     critical_value = CharField(max_length=200, null=False, default='')
#     active_sw = BooleanField(default=True, null=False)
#     created_dttm = DateTimeField(editable=False, auto_now_add=True)
#     updated_dttm = DateTimeField(auto_now=True)
#
#
# # =========================================================================================
# #      Issue is when someone could be notified in some manor due to metrics_temp passing over a threshold
# # =========================================================================================
# class IssueTracker(models.Model):
#     class Meta:
#         db_table = 'issue_tracker'
#         ordering = ['-start_dttm']
#
#     server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
#     checker_threshold = ForeignKey(CheckerThreshold, on_delete=deletion.ProtectedError, null=False, default='')
#     start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
#     last_dttm = DateTimeField(auto_now=True)
#     closed_sw = BooleanField(default=False)
#     pending_status = CharField(max_length=15, null=False, default='', choices=IssueStatusChoices.choices)
#     current_status = CharField(max_length=15, null=False, default='', choices=IssueStatusChoices.choices)
#     element_details = CharField(max_length=25, null=False, default='')
#     critical_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
#     warning_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
#     normal_ticks = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)], null=False, default=0)
#     note = CharField(max_length=4000, null=True, default='')
#     note_by = CharField(max_length=30, null=True, default='')
#     ticket = CharField(max_length=30, null=True, default='')
#     created_dttm = DateTimeField(editable=False, auto_now_add=True)
#     updated_dttm = DateTimeField(auto_now=True)
#
#
# class IssueNotification(models.Model):
#     class Meta:
#         db_table = 'issue_notification'
#
#     issue_tracker = ForeignKey(IssueTracker, on_delete=deletion.CASCADE, null=True)
#     application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=True)
#     notification_dttm = DateTimeField(editable=False, auto_now_add=True)
#     notification_method = ForeignKey(ThresholdNotificationMethodLookup, on_delete=CASCADE, default='')
#     notification_subject = CharField(max_length=2000, null=False, default='')
#     notification_body = CharField(max_length=10000, null=False, default='')
#     acknowledged_by = CharField(max_length=30, null=False, default='')
#     acknowledged_dttm = DateTimeField(null=False, default=INFINITY)
#     created_dttm = DateTimeField(editable=False, auto_now_add=True)
#     updated_dttm = DateTimeField(auto_now=True)
