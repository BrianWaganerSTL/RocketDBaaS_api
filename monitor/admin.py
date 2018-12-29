from django.contrib import admin

# ====================================================================
from monitor.models import *


@admin.register(ThresholdNotificationMethodLookup)
class ThresholdNotificationMethodLookup(admin.ModelAdmin):
    list_display = [field.attname for field in ThresholdNotificationMethodLookup._meta.fields]


@admin.register(ThresholdCategoryLookup)
class ThresholdCategoryLookup(admin.ModelAdmin):
    list_display = [field.attname for field in ThresholdCategoryLookup._meta.fields]

@admin.register(ThresholdMetricLookup)
class ThresholdMetricLookup(admin.ModelAdmin):
    list_display = [field.attname for field in ThresholdMetricLookup._meta.fields]


@admin.register(ThresholdTest)
class ThresholdTest(admin.ModelAdmin):
    list_display = [field.attname for field in ThresholdTest._meta.fields]


@admin.register(Incident)
class Incident(admin.ModelAdmin):
    list_display = [field.attname for field in Incident._meta.fields]


@admin.register(IncidentNotification)
class IncidentNotification(admin.ModelAdmin):
    list_display = [field.attname for field in IncidentNotification._meta.fields]
