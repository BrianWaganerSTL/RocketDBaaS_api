from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ng.views.views import CreateDBInit, MyPoolServersViewSet
from ng.views.createClusterViewSet import ClusterViewSet

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)
router.register(r'clusters', ClusterViewSet)

urlpatterns = router.urls