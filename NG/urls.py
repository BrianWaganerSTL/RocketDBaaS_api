from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateDBInit, MyPoolServersViewSet

router = DefaultRouter()
router.register(r'MyPoolServers', MyPoolServersViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('createDB', CreateDBInit)
]