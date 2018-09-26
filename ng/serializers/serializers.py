from rest_framework import serializers
from .models import (
    PoolServer
)

class LockPoolServersSerializer (serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'mem_gb', 'db_gb',
                  'data_center', 'status_in_pool', 'created_dttm', 'updated_dttm' )
        extra_kwargs = {
            'url': {'lookup_field': 'dbms_type'}},


class LockPoolServers2Serializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'mem_gb', 'db_gb',
                  'data_center', 'status_in_pool', 'created_dttm', 'updated_dttm')
        extra_kwargs = {
            'url': {'lookup_field': 'needed_servers'}}

class MyPoolServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'mem_gb', 'db_gb', 'data_center', 'status_in_pool')
