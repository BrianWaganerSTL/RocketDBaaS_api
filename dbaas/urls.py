from django.urls import path
from rest_framework.routers import DefaultRouter


from dbaas.views import ApiViews
from metrics import metrics_views
from monitor import monitor_views

router = DefaultRouter()
router.register(r'poolservers', ApiViews.PoolServersViewSet)
router.register(r'clusters', ApiViews.Clusters)

urlpatterns = [
    path('applications/<vApplicationId>/contacts/', ApiViews.ApplicationContactsList.as_view()),
    path('clusters/<vClusterId>/servers/', ApiViews.ServersList.as_view()),
    path('clusters/<vClusterId>/backups/', ApiViews.BackupsList.as_view()),
    path('clusters/<vClusterId>/restores/', ApiViews.RestoresList.as_view()),
    path('clusters/<vClusterId>/notes/', ApiViews.NotesList.as_view()),
    path('servers/<vServerId>/activities/', ApiViews.ActivitiesList.as_view()),
    path('dbmstypes/', ApiViews.DbmsTypesList),
    path('environments/', ApiViews.EnvironmentsList.as_view()),

    path('servers/<vServerId>/incidents/', monitor_views.IncidentList.as_view()),

    path('servers/<vServerId>/metrics/cpu/', metrics_views.Metrics_CpuList.as_view()),
    path('servers/<vServerId>/metrics/mountpoints/', metrics_views.Metrics_MountPointList.as_view()),
    path('servers/<vServerId>/metrics/load/', metrics_views.Metrics_CpuLoadList.as_view()),
    path('servers/<vServerId>/metrics/pingserver/', metrics_views.Metrics_PingServerList.as_view()),
    path('servers/<vServerId>/metrics/pingdb/', metrics_views.Metrics_PingDbList.as_view()),
]

urlpatterns += router.urls
