from rest_framework import serializers
from dbaas.models import (PoolServer)



class LockPoolServersSerializer (serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'ram_gb', 'db_gb',
                  'datacenter', 'status_in_pool', 'created_dttm', 'updated_dttm' )
        extra_kwargs = {
            'url': {'lookup_field': 'dbms_type'}},


class LockPoolServers2Serializer(serializers.ModelSerializer):
    class Meta:
        model = PoolServer
        fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'ram_gb', 'db_gb',
                  'datacenter', 'status_in_pool', 'created_dttm', 'updated_dttm')
        extra_kwargs = {
            'url': {'lookup_field': 'needed_servers'}}

# class MyPoolServersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PoolServer
#         fields = ('server_name', 'server_ip', 'dbms_type', 'cpu', 'ram_gb', 'db_gb', 'datacenter', 'status_in_pool', 'cluster')
