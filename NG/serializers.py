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
            'url': {'lookup_field': 'dbmsType'}}