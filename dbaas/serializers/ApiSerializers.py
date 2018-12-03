from rest_framework import serializers
from dbaas.models import Cluster, Server, PoolServer, Backup, Restore, ServerActivity, ClusterNote, ApplicationContact, Issue


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


class ApplicationContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationContact
        fields = '__all__'
        depth = 1


class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ('id', 'cluster_name', 'dbms_type', 'application', 'environment', 'requested_cpu', 'requested_ram_gb',
                  'requested_db_gb', 'read_write_port', 'read_only_port', 'tls_enabled_sw', 'backup_retention_days',
                  'cluster_health', 'active_sw', 'eff_dttm', 'exp_dttm', 'created_dttm', 'updated_dttm')
        # fields = '__all__'
        depth = 1


class PoolServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = '__all__'
        depth = 0


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        depth = 2
        sorted('created_dttm', reverse=True)