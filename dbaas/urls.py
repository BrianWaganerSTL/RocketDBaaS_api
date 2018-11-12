from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dbaas.views import overview_view, cluster_details_view, pool_servers_views, create_cluster_view, ApiViews
from dbaas.views.views import MyPoolServersViewSet
from dbaas.views.ApiViews import Clusters
from dbaas.views.create_cluster_view import create_cluster
from dbaas.views.ApiViews import Clusters

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ApiViews.Clusters)

urlpatterns = [
    path('clusters/<vClusterId>/servers/', ApiViews.ServersList.as_view()),
    path('overview/', overview_view.overview, name='overview'),
    path('cluster_details/<_cluster_id>', cluster_details_view.cluster_details, name='cluster_details'),

    path('clusters/<vClusterId>/backups/', ApiViews.BackupsList.as_view()),
    path('clusters/<vClusterId>/restores/', ApiViews.RestoresList.as_view()),
    path('clusters/<vClusterId>/activities/', ApiViews.ActivitiesList.as_view()),
    path('clusters/<vClusterId>/notes/', ApiViews.NotesList.as_view()),
    path('clusters/<vClusterId>/alerts/', ApiViews.AlertsList.as_view()),
    path('applications/<vApplicationId>/contacts/', ApiViews.ApplicationContactsList.as_view()),
    path('applications/<vApplicationId>/contactsView/', ApiViews.ApplicationContactsViewList.as_view()),

    path('pool_servers/', pool_servers_views.pool_servers, name='pool_servers'),
    path('cluster/create', create_cluster_view.create_cluster, name='cluster/create.html'),
    path('', overview_view.overview, name='overview'),
]

urlpatterns += router.urls
