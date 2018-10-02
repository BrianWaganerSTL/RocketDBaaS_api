"""RocketDBaaS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from rest_framework import routers
#from dbaas.views import *
from dbaas.views import overview_view
from dbaas.controllers import *
from dbaas import urls

# router = routers.DefaultRouter()
# #router.register(r'dbms/mongoDB/lockPoolServers', LockPoolServersViewSet)
# router.register(r'MyPoolServers', MyPoolServersViewSet)
#router.register(r'createDB', MyPoolServersViewSet)

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', admin.site.urls),
#     # path('api/', include(router.urls)),
#     path('api/ClaimPoolServers', ClaimPoolServers),
#     path('api/profile/<int:NeededServers>/', profile),
#     path('api/profile/', profile),
# ]
urlpatterns = [
     path('api/', include('dbaas.urls')),
     path('dbaas/', include('dbaas.urls')),
     path('admin/', admin.site.urls),
     path('api-auth/', include('rest_framework.urls')),
     path('', overview_view.overview),
     # path('auth_api/', include('auth_api.urls'))
     # TODO: The Reset not quite working, I suspect it is expecting you are logged in
     path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset',),
     path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done',),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete',),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



