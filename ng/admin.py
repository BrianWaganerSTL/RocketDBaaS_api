from django.contrib import admin

from .models import *


@admin.register(PoolServer)
class PoolServer(admin.ModelAdmin):
    list_display = ('id','status_in_pool', 'dbms_type', 'server_name', 'cpu', 'mem_gb', 'db_gb')
    list_editable = ('status_in_pool',)
    list_display_links = ('id',)


@admin.register(Application)
class Application(admin.ModelAdmin):
    list_display = ('id','application_name', 'active_sw')
    list_editable = ('application_name', 'application_name')
    list_display_links = ('id',)


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('contact_name','active_sw')
    list_display_links = ('contact_name',)


@admin.register(ApplicationContact)
class ApplicationContact(admin.ModelAdmin):
    list_display = ('id','application','contact')
    list_select_related = ('application','contact',)
    list_display_links = ('id',)


@admin.register(Cluster)
class Cluster(admin.ModelAdmin):
    list_display = ('cluster_name','dbms_type','application','environment','cluster_health','active_sw')
    list_select_related = ('application',)
    list_display_links = ('cluster_name',)


@admin.register(Server)
class Server(admin.ModelAdmin):
    list_display = ('cluster', 'server_name','server_ip','cpu','mem_gb','db_gb','data_center','node_role','os_version','db_version','pending_restart_sw','active_sw')
    list_select_related = ('cluster',)
    list_display_links = ('server_name',)

