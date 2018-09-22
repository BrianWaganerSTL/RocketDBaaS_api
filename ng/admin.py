from django.contrib import admin

from .models import *
admin.site.register(Application)
admin.site.register(Server)

@admin.register(PoolServer)
class PoolServer(admin.ModelAdmin):
    list_display = ('status_in_pool','dbms_type','server_name','cpu','mem_gb','db_gb')
    list_editable = ('status_in_pool',)
    list_display_links = ('server_name',)


@admin.register(ApplicationContact)
class ApplicationContact(admin.ModelAdmin):
    list_display = ('application','contact')
    list_display_links = ('application',)

@admin.register(Contact)
class Contact(admin.ModelAdmin):
    list_display = ('contact_name','active_sw')
    list_display_links = ('contact_name',)

@admin.register(Cluster)
class Cluster(admin.ModelAdmin):
    list_display = ('cluster_name','dbms_type','application','environment','health','active_sw')
    list_display_links = ('cluster_name',)