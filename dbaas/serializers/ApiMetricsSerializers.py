from rest_framework import serializers
from dbaas.models import MetricsCpu, MetricsPingServer, MetricsMountPoint, \
    MetricsLoad, MetricsPingDb, CheckerThreshold


class MetricsCpuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsCpu
        fields = '__all__'
        depth = 0

class MetricsMountPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsMountPoint
        fields = '__all__'
        depth = 0

class MetricsLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsLoad
        fields = '__all__'
        depth = 0

class MetricsPingServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsPingServer
        fields = '__all__'
        depth = 0

class MetricsPingDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricsPingDb
        fields = '__all__'
        depth = 0


class MetricThresholdSerializer (serializers.ModelSerializer):
    class Meta:
        model = CheckerThreshold
        fields = '__all__'
        depth = 2