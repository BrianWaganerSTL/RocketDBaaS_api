from django.contrib.auth.models import User
from django.contrib.contenttypes import fields
from django.db.models.fields import reverse_related
from rest_framework import serializers
# from rest_framework.serializers.ModelSerializer import build
from ng.models import Cluster, Server, PoolServer


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('id', 'cluster_name', 'dbms_type', 'application', 'environment', 'requested_cpu', 'requested_mem_gb', 'requested_db_gb',
                  'haproxy_port', 'tls_enabled_sw', 'backup_retention_days')


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('id', 'cluster', 'server_name', 'server_ip', 'cpu', 'mem_gb', 'db_gb', 'data_center', 'node_role')
#        serializers.ModelSerializer.build_nested_field(ClusterSerializer, 'cluster', reverse_related.ForeignObjectRel, 2)


class PoolServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('id','environment', 'server_name', 'server_ip', 'dbms_type', 'cpu', 'mem_gb', 'db_gb', 'data_center', 'status_in_pool')


# def create(self, validated_data):
#     tmp_post = validated_data
#     user = None
#
#     request = self.context.get("request")
#     if request and hasattr(request, "user"):
#         user = request.user
#
#     cluster = Cluster.objects.create(
#         user=user,
#         title=tmp_post['title'],
#         text=tmp_post['text'],
#     )
#
#     return cluster


