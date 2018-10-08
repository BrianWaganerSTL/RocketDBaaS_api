from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dbaas.views import overview_view, cluster_details_view, pool_servers_views, create_cluster_view
from dbaas.views.views import MyPoolServersViewSet
from dbaas.views.createClusterViewSet import ClusterViewSet
from dbaas.views.create_cluster_view import create_cluster

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'servers', ClusterViewSet)

urlpatterns = [
    path('overview/', overview_view.overview, name='overview'),
    path('cluster_details/<_cluster_id>', cluster_details_view.cluster_details, name='cluster_details'),
    path('pool_servers/', pool_servers_views.pool_servers, name='pool_servers'),
    path('cluster/create', create_cluster_view.create_cluster, name='cluster/create.html'),
    path('', overview_view.overview, name='overview'),
]

urlpatterns += router.urls
