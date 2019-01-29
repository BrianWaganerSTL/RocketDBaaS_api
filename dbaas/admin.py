from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .models import *


@admin.register(Datacenter)
class Datacenter(admin.ModelAdmin):
    list_display = [field.attname for field in Datacenter._meta.fields]
    list_editable = ('datacenter','order_num')
    list_display_links = ()

@admin.register(Environment)
class Environment(admin.ModelAdmin):
    list_display = [field.attname for field in Environment._meta.fields]

@admin.register(ServerPort)
class ServerPort(admin.ModelAdmin):
    list_display = [field.attname for field in ServerPort._meta.fields]
    list_display_links = ('port',)
    ordering = ['port']


@admin.register(Application)
class Application(admin.ModelAdmin):
    list_display = ('id','application_name', 'active_sw')
    list_editable = ('application_name', )
    list_display_links = ('id',)


@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('contact_name','contact_email','contact_phone','active_sw')
    list_display_links = ('contact_name',)


@admin.register(ApplicationContact)
class ApplicationContact(admin.ModelAdmin):
    list_display = ('id','application_id','contact_id','active_sw')
    list_display_links = ('id',)


@admin.register(Cluster)
class Cluster(admin.ModelAdmin):
    list_display = [field.attname for field in Cluster._meta.fields]


@admin.register(Server)
class Server(admin.ModelAdmin):
    list_display = [field.attname for field in Server._meta.fields]


@admin.register(ServerActivity)
class ServerActivity(admin.ModelAdmin):
    list_display = ('server', 'activity_type','activity_status','start_dttm')
    list_select_related = ('server',)
    list_display_links = ('server',)


@admin.register(ClusterNote)
class ClusterNote(admin.ModelAdmin):
    list_display = ('cluster', 'title', 'note', 'created_dttm', 'updated_dttm')
    list_select_related = ('cluster',)
    list_display_links = ('cluster',)


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


# ====================================================================
AdminSite.site_title="Rocket DBaaS"
AdminSite.site_header = 'Rocket DBaaS Administration'

