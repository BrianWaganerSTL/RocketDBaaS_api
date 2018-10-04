from django.contrib import admin

from django.contrib.admin.sites import AdminSite

from .models import *


@admin.register(PoolServer)
class PoolServer(admin.ModelAdmin):
    list_display = ('id','status_in_pool', 'dbms_type', 'server_name', 'cpu', 'mem_gb', 'db_gb')
    list_editable = ('status_in_pool',)
    list_display_links = ('id',)


@admin.register(ServerPort)
class ServerPort(admin.ModelAdmin):
    list_display = ('port', 'port_status','port_notes','updated_dttm')
    list_select_related = ('port',)
    list_display_links = ('port',)


@admin.register(Application)
class Application(admin.ModelAdmin):
    list_display = ('id','application_name', 'active_sw')
    list_editable = ('application_name', 'application_name')
    list_display_links = ('id',)


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('contact_name','contact_email','contact_phone','active_sw')
    list_display_links = ('contact_name',)


@admin.register(ApplicationContact)
class ApplicationContact(admin.ModelAdmin):
    list_display = ('id','application','contact')
    list_select_related = ('application','contact',)
    list_display_links = ('id',)


@admin.register(Cluster)
class Cluster(admin.ModelAdmin):
    list_display = ('cluster_name','dbms_type','application','environment','cluster_health','active_sw',
                    'read_write_port','read_only_port')
    list_select_related = ('application',)
    list_display_links = ('cluster_name',)


@admin.register(Server)
class Server(admin.ModelAdmin):
    list_display = ('cluster', 'server_name','server_ip','cpu','mem_gb','db_gb','data_center','node_role','os_version',
                    'db_version','pending_restart_sw','active_sw')
    list_select_related = ('cluster',)
    list_display_links = ('server_name',)

@admin.register(Backup)
class Backup(admin.ModelAdmin):
    list_display = ('cluster', 'backup_type','backup_status','db_size_gb','backup_size_gb')
    list_select_related = ('cluster',)
    list_display_links = ('cluster',)


@admin.register(Restore)
class Restore(admin.ModelAdmin):
    list_display = ('from_cluster', 'to_cluster','restore_type','restore_to_dttm','restore_status','start_dttm')
    list_select_related = ('from_cluster','to_cluster',)
    list_display_links = ('from_cluster',)


@admin.register(ServerActivities)
class ServerActivities(admin.ModelAdmin):
    list_display = ('server', 'server_activity','activity_status','start_dttm')
    list_select_related = ('server',)
    list_display_links = ('server',)

@admin.register(ClusterNote)
class ClusterNotes(admin.ModelAdmin):
    list_display = ('cluster', 'title', 'note', 'created_dttm', 'updated_dttm')
    list_select_related = ('cluster',)
    list_display_links = ('cluster',)


AdminSite.site_title="Rocket DBaaS"
AdminSite.site_header = 'Rocket DBaaS Administration'

