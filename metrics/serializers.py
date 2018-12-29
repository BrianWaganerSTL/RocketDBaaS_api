from rest_framework import serializers
from metrics.models import Metrics_Cpu, Metrics_PingServer, Metrics_MountPoint, \
    Metrics_CpuLoad, Metrics_PingDb


class Metrics_CpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics_Cpu
        fields = '__all__'
        depth = 0

class Metrics_MountPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics_MountPoint
        fields = '__all__'
        depth = 0

class Metrics_CpuLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics_CpuLoad
        fields = '__all__'
        depth = 0

class Metrics_PingServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics_PingServer
        fields = '__all__'
        depth = 0

class Metrics_PingDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metrics_PingDb
        fields = '__all__'
        depth = 0