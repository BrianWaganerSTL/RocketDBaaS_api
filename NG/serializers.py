from rest_framework import serializers
from .models import (
    PoolServer
)

class LockPoolServersSerializer (serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('serverName', 'serverIp', 'dbmsType', 'cpu', 'memGigs', 'dbGigs',
                  'dataCenter', 'statusInPool', 'createdDttm', 'updatedDttm' )
        extra_kwargs = {
            'url': {'lookup_field': 'dbmsType'}},


class LockPoolServers2Serializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('serverName', 'serverIp', 'dbmsType', 'cpu', 'memGigs', 'dbGigs',
                  'dataCenter', 'statusInPool', 'createdDttm', 'updatedDttm')
        extra_kwargs = {
            'url': {'lookup_field': 'needed_servers'}}

class MyPoolServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('serverName', 'serverIp', 'dbmsType', 'cpu', 'memGigs', 'dbGigs', 'dataCenter', 'statusInPool')
