
from rest_framework import serializers

from monitor.models import ThresholdTest, Incident


class ThresholdTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThresholdTest
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
        depth = 2
        sorted('created_dttm', reverse=True)