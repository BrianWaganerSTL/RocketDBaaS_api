from rest_framework import serializers

from dbaas.models import Cluster, Server, ApplicationContact

class ClusterDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'
        depth = 5
