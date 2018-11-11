from django.contrib.auth.models import User
from django.contrib.contenttypes import fields
from django.db.models.fields import reverse_related
from rest_framework import serializers
from dbaas.models import Cluster, Server, PoolServer, Backup, Restore, ServerActivity, ClusterNote, Alert


class ServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'
        depth = 0

class BackupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)

class RestoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restore
        fields = '__all__'
        depth = 1
        sorted('created_dttm', reverse=True)

class ServerActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerActivity
        fields = '__all__'
        depth = 1
        sorted('created_dttm', reverse=True)

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterNote
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)

class AlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('id', 'cluster_name', 'dbms_type', 'application', 'environment', 'requested_cpu', 'requested_mem_gb',
                  'requested_db_gb', 'read_write_port', 'read_only_port', 'tls_enabled_sw', 'backup_retention_days',
                  'cluster_health', 'active_sw', 'eff_dttm', 'exp_dttm', 'created_dttm', 'updated_dttm')
        # fields = '__all__'
        depth = 1


# class ClusterServersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Server
#         fields = ('id','cluster_id','server_name','server_ip','cpu','mem_gb','db_gb','data_center','node_role','server_health','os_version','db_version','pending_restart_sw','active_sw','created_dttm','updated_dttm')
#         depth = 0



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


