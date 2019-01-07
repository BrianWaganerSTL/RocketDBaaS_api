"""RocketDBaaS_api URL Configuration

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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from rest_framework.authtoken import views

from RocketDBaaS.master_scheduler import StartMasterScheduler
from dbaas.controllers import *

urlpatterns = [
  path('dbaas/', include('dbaas.urls')),
  path('dbaas_api/', admin.site.urls),
  url(r'dbaas_api/api-token-auth/', views.obtain_auth_token),
  path('dbaas_api/auth/', include('rest_framework.urls')),
  # path('auth_api/', include('auth_api.urls'))
  # TODO: The Reset not quite working, I suspect it is expecting you are logged in
  path('dbaas_api/admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
  path('dbaas_api/admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
  path('dbaas_api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
  path('dbaas_api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

StartMasterScheduler()

