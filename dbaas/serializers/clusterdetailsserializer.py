from rest_framework import serializers

from dbaas.models import Cluster, Server, ApplicationContact

class ClusterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'
        # fields = ('id', 'cluster_name', 'dbms_type', 'application', 'environment', 'requested_cpu', 'requested_mem_gb', 'requested_db_gb',
        #           'haproxy_port', 'tls_enabled_sw', 'backup_retention_days')
        depth = 3


