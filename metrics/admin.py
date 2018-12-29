from django.contrib import admin

from metrics.models import Metrics_Cpu, Metrics_MountPoint, Metrics_CpuLoad, Metrics_PingDb, Metrics_PingServer


@admin.register(Metrics_Cpu)
class Metrics_CPU(admin.ModelAdmin):
    list_display = [field.attname for field in Metrics_Cpu._meta.fields]


@admin.register(Metrics_MountPoint)
class Metrics_MountPoint(admin.ModelAdmin):
    list_display = [field.attname for field in Metrics_MountPoint._meta.fields]


@admin.register(Metrics_CpuLoad)
class Metrics_CpuLoad(admin.ModelAdmin):
    list_display = [field.attname for field in Metrics_CpuLoad._meta.fields]


@admin.register(Metrics_PingDb)
class Metrics_PingDb(admin.ModelAdmin):
    list_display = [field.attname for field in Metrics_PingDb._meta.fields]


@admin.register(Metrics_PingServer)
class Metrics_ServerPing(admin.ModelAdmin):
    list_display = [field.attname for field in Metrics_PingServer._meta.fields]

