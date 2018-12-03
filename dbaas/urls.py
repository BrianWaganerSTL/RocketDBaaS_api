from django.urls import path
from rest_framework.routers import DefaultRouter

from dbaas.views import ApiViews, ApiMetricsViews

router = DefaultRouter()
router.register(r'poolservers', ApiViews.PoolServersViewSet)
router.register(r'clusters', ApiViews.Clusters)
# TODO: Chage the below to servers/<vServerId>/metrics/cpu
# router.register(r'servers/metrics/cpu', ApiViews.MetricsCpuViewSet)

urlpatterns = [
    path('clusters/<vClusterId>/servers/', ApiViews.ServersList.as_view()),
    path('clusters/<vClusterId>/backups/', ApiViews.BackupsList.as_view()),
    path('clusters/<vClusterId>/restores/', ApiViews.RestoresList.as_view()),
    path('clusters/<vClusterId>/activities/', ApiViews.ActivitiesList.as_view()),
    path('clusters/<vClusterId>/notes/', ApiViews.NotesList.as_view()),
    path('servers/<vServerId>/metrics/cpu/', ApiMetricsViews.MetricsCpuList.as_view()),
    path('servers/<vServerId>/metrics/mountpoint/', ApiMetricsViews.MetricsMountPointList.as_view()),
    path('servers/<vServerId>/metrics/load/', ApiMetricsViews.MetricsLoadList.as_view()),
    path('servers/<vServerId>/metrics/pingserver/', ApiMetricsViews.MetricsPingServerList.as_view()),
    path('servers/<vServerId>/metrics/pingdb/', ApiMetricsViews.MetricsPingDbList.as_view()),
    path('servers/<vServerId>/issues/', ApiViews.IssuesList.as_view()),
    path('applications/<vApplicationId>/contacts/', ApiViews.ApplicationContactsList.as_view()),
]

urlpatterns += router.urls
