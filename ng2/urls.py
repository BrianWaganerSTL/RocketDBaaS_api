from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ng2.views import overview_view, cluster_details_view, pool_servers_views
from ng2.views.views import MyPoolServersViewSet
from ng2.views.createClusterViewSet import ClusterViewSet

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'servers', ClusterViewSet)

urlpatterns = [
    path('overview/', overview_view.overview, name='overview'),
    path('cluster_details/<_cluster_id>', cluster_details_view.cluster_details, name='cluster_details'),
    path('pool_servers/', pool_servers_views.pool_servers, name='pool_servers'),
    path('', overview_view.overview, name='overview'),
]

urlpatterns += router.urls