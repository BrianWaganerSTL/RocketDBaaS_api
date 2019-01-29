import logging

from django.core.exceptions import ValidationError, FieldDoesNotExist, FieldError
from django.db import IntegrityError
from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from dbaas.models import Cluster, Server, Backup, Restore, ServerActivity, ClusterNote, ApplicationContact, Contact, Environment, Application, ServerPort


class EnvironmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'
        depth = 0
        sorted('order_num')

class ApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        depth = 1
        sorted('application_name')
        # extra_kwargs = {'url': {'lookup_field': 'application_name'}},


class ServersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = '__all__'
        depth = 1


class BackupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)


class RestoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restore
        fields = '__all__'
        depth = 1
        sorted('created_dttm', reverse=True)


class ServerActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerActivity
        fields = '__all__'
        depth = 1
        sorted('created_dttm', reverse=True)


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClusterNote
        fields = '__all__'
        depth = 0
        sorted('created_dttm', reverse=True)


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        depth = 1


class ApplicationContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationContact
        fields = '__all__'
        depth = 1


class ClusterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cluster
    fields = '__all__'
    depth = 3
    read_only_fields = ['application','environment']


  def create(self, validated_data):
    appl_name = self.initial_data['application_name']
    application = Application()
    if (Application.objects.filter(application_name=appl_name).count() == 0):
      print('No Application found.  Create a new one')
      logging.info('No Application found.  Create a new one');
      application.application_name = appl_name
      application.active_sw = True
      application.save()

    application = get_object_or_404(Application.objects.filter(application_name=appl_name))
    print('In ClusterSerializer(POST). application.id=' + str(application.id))
    logging.info('In ClusterSerializer(POST). application.id=', application.id)
    validated_data.update(application_id=application.id)  # Add it to the object to be saved

    env_name = self.initial_data['environment_name']
    if (Environment.objects.filter(env_name=env_name) == 0): # It's a natural key)
      raise ValidationError("Error: env_name(" + env_name + ") doesn't exist")

    validated_data.update(environment_id=env_name)  # Add it to the object to be saved

    read_write_port = ServerPort.NextOpenPort(self)
    read_write_port.updated_dttm = timezone.datetime.now()
    read_write_port.port_status = ServerPort.PortStatusChoices.LOCKED
    read_write_port.save()
    read_write_port.port_status = ServerPort.PortStatusChoices.USED
    validated_data.update(read_write_port=read_write_port)

    read_only_port = ServerPort.NextOpenPort(self)
    read_write_port.updated_dttm = timezone.datetime.now()
    read_only_port.port_status = ServerPort.PortStatusChoices.LOCKED
    read_only_port.save()
    read_only_port.port_status = ServerPort.PortStatusChoices.USED
    validated_data.update(read_only_port=read_only_port)

    # Just validate the server for now
    server_ids = self.initial_data['server_ids']
    for id in server_ids:
      try:
        server = Server.objects.filter(pk=id, cluster_id__isnull=True, node_role=Server.NodeRoleChoices.POOLSERVER)
      except Exception as e:
        raise ValidationError("Error: server_id(" + id + ") doesn't exist and/or belongs to a cluster and/or is not a PoolServer" + str(e))

    cluster = Cluster.objects.create(**validated_data)
    print(str(cluster))
    cluster.save()

    server = Server()
    for id in server_ids:
      server = Server()
      try:
        server = get_object_or_404(Server.objects.filter(id=id))
      except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
        print('No Server (" + id + ") found to join the cluster. ' + str(ex))
      server.cluster_id = cluster.id
      server.node_role = Server.NodeRoleChoices.CONFIGURING
      server.save()

    return cluster
