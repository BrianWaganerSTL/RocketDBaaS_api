from django.contrib import admin

from .models import *


admin.site.register(PoolServer)
admin.site.register(Environment)
admin.site.register(Contact)
admin.site.register(Application)
admin.site.register(Server)
admin.site.register(Cluster)
admin.site.register(ApplicationContact)
