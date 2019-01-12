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
# from rest_auth.registration import urls
from rest_framework.authtoken import views
from rest_framework_swagger.views import get_swagger_view

from RocketDBaaS.master_scheduler import StartMasterScheduler
from dbaas.controllers import *

urlpatterns = [
    path('dbaas_api/', include('dbaas.urls')),
    path('admin/', admin.site.urls),
    url(r'dbaas_api/api-token-auth/', views.obtain_auth_token),

    path('dbaas_api/auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', rest_auth.registration.urls),
    # # https://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html
    # path('/rest-auth/login/', include('rest_auth.urls')),
    # # (POST) username, email, password   Returns Token key
    # path('/rest-auth/login/', include('rest_auth.urls')),
    # # (POST)
    # path('/rest-auth/user/', include('rest_auth.urls')),
    # # (GET, PUT, PATCH) username, first_name, last_nane   Returns pk, username, email, first_name, last_name
    # path('/rest-auth/registration/', include('rest_auth.urls')),
    # # (POST) username, password1, password2, email

    url(r'^docs/$', get_swagger_view(title='RocketDBaaS API Docs'), name='api_docs'),

    # path('auth_api/', include('auth_api.urls'))
    # TODO: The Reset not quite working, I suspect it is expecting you are logged in
    path('dbaas_api/admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset', ),
    path('dbaas_api/admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done', ),
    path('dbaas_api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm', ),
    path('dbaas_api/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete', ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

StartMasterScheduler()
