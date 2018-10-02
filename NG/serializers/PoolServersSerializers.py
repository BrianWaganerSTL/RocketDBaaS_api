from rest_framework import serializers

from ng.models2 import Cluster, Server, ApplicationContact

class PoolServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = '__all__'
        depth = 3

