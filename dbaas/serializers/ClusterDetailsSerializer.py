from rest_framework import serializers

from dbaas.models import Cluster, Server, ApplicationContact

class ClusterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        # fields = '__all__'
        fields = ('id', 'cluster_name', 'dbms_type', 'application', 'environment', 'tls_enabled_sw')
        depth = 5