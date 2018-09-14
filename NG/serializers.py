from rest_framework import serializers
from .models import (
    PoolServer
)

class PoolServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('serverName', 'serverIp', 'dbms', 'cpu', 'memGigs', 'dbGigs', 'dataCenter', 'statusInPool', 'createdDttm', 'updatedDttm' )