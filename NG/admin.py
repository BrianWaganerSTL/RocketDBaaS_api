from django.contrib import admin

from .models import *


admin.site.register(Environment)
admin.site.register(Application)
admin.site.register(Server)

@admin.register(PoolServer)
class PoolServer(admin.ModelAdmin):
    list_display = ('statusInPool','dbmsType','serverName','cpu','memGigs','dbGigs')
    list_editable = ('statusInPool',)
    list_display_links = ('serverName',)

@admin.register(ApplicationContact)
class ApplicationContact(admin.ModelAdmin):
    list_display = ('application','contact')
    list_display_links = ('application',)

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('contactName','activeSw')
    list_display_links = ('contactName',)

@admin.register(Cluster)
class Cluster(admin.ModelAdmin):
    list_display = ('clusterName','dbmsType','application','environment','activeSw')
    list_display_links = ('clusterName',)