from django.urls import path
from rest_framework.routers import DefaultRouter

from dbaas.views import ApiViews
from metrics import metrics_views
from metrics.services.charts import mountPoints, cpu
from monitor import monitor_views

router = DefaultRouter()
router.register(r'poolservers', ApiViews.PoolServersViewSet)
router.register(r'clusters', ApiViews.Clusters)
router.register(r'servers', ApiViews.Servers)
router.register(r'applications', ApiViews.Applications)
router.register(r'environments', ApiViews.Environments)
router.register(r'threshold_tests', monitor_views.ThresholdTest)
# http://127.0.0.1:8080/admin/dbaas/cluster/add/
urlpatterns = [
  path('applications/<vApplicationId>/contacts/', ApiViews.ApplicationContactsList.as_view()),
  path('clusters/<vClusterId>/servers/', ApiViews.ServersList.as_view()),
  path('clusters/<vClusterId>/backups/', ApiViews.BackupsList.as_view()),
  path('clusters/<vClusterId>/restores/', ApiViews.RestoresList.as_view()),
  path('clusters/<vClusterId>/notes/', ApiViews.NotesList.as_view()),
  path('servers/<vServerId>/activities/', ApiViews.ActivitiesList.as_view()),
  path('dbmstypes/', ApiViews.DbmsTypesList),

  path('servers/<vServerId>/incidents/', monitor_views.IncidentList.as_view()),

  path('servers/<vServerId>/metrics/cpu/', metrics_views.Metrics_CpuList.as_view()),
  path('servers/<vServerId>/metrics/mountpoints/', metrics_views.Metrics_MountPointList.as_view()),
  path('servers/<vServerId>/metrics/load/', metrics_views.Metrics_CpuLoadList.as_view()),
  path('servers/<vServerId>/metrics/pingserver/', metrics_views.Metrics_PingServerList.as_view()),
  path('servers/<vServerId>/metrics/pingdb/', metrics_views.Metrics_PingDbList.as_view()),

  path('servers/<vServerId>/charts/mountpoints/', mountPoints.ChartMountPoints.as_view()),
  path('servers/<vServerId>/charts/cpus/', cpu.ChartCpus.as_view()),
]

urlpatterns += router.urls
