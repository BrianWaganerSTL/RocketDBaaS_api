from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

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
    # fields = ('cluster_name','dbms_type','application','environment','read_write_port','read_only_port','tls_enabled_sw','backup_retention_days','cluster_health','active_sw','eff_dttm','exp_dttm','created_dttm','updated_dttm')
    depth = 2
    read_only_fields = ['application','environment']

  def validate_application(self, pk):
    try:
      data = Application.objects.get(id=pk)
    except Exception as e:
      raise ValidationError("Error: application_id("+pk+") doesn't exist")
    return data

  def validate_environement(self, pk):
    try:
      data = Environment.objects.get(env_name=pk)  # It's a natural key
    except Exception as e:
      raise ValidationError("Error: environment_id("+pk+") doesn't exist")
    return data

  def create(self, validated_data):

    pk = self.initial_data['application_id']
    self.validate_application(pk)
    validated_data.update(application_id=pk)

    pk = self.initial_data['environment']
    self.validate_environement(pk)
    validated_data.update(environment_id=pk)

    read_write_port = ServerPort.NextOpenPort(self)
    read_write_port.updated_dttm = timezone.datetime.now()
    read_write_port.port_status = ServerPort.PortStatusChoices.Locked
    read_write_port.save()
    read_write_port.port_status = ServerPort.PortStatusChoices.Used
    validated_data.update(read_write_port=read_write_port)

    read_only_port = ServerPort.NextOpenPort(self)
    read_write_port.updated_dttm = timezone.datetime.now()
    read_only_port.port_status = ServerPort.PortStatusChoices.Locked
    read_only_port.save()
    read_only_port.port_status = ServerPort.PortStatusChoices.Used
    validated_data.update(read_only_port=read_only_port)

    cluster = Cluster.objects.create(**validated_data)
    cluster.save()

    return cluster
