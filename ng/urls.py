from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from NextGenDB1 import settings
from ng.views import homeViews, cluster_details_view
from ng.views.views import CreateDBInit, MyPoolServersViewSet
from ng.views.createClusterViewSet import ClusterViewSet

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ClusterViewSet)
router.register(r'servers', ClusterViewSet)

urlpatterns = [
    url('home$', homeViews.homeView),
    path('cluster_details/<cluster_name>', cluster_details_view.cluster_details, name='cluster_details'),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += router.urls