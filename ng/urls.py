from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from NextGenDB1 import settings
from ng.views import overview_view, cluster_details_view
from ng.views.views import CreateDBInit, MyPoolServersViewSet
from ng.views.createClusterViewSet import ClusterViewSet

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'servers', ClusterViewSet)

urlpatterns = [
    # path('home', homeViews.homeView, name='home'),
    path('overview/', overview_view.overview, name='overview'),
    path('cluster_details/<_cluster_id>', cluster_details_view.cluster_details, name='cluster_details'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += router.urls