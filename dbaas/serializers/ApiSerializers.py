from rest_framework import serializers
from dbaas.models import Cluster, Server, Backup, Restore, ServerActivity, ClusterNote, ApplicationContact, Contact, DbmsTypeChoices, Environment


class EnvironmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'
        depth = 0
        sorted('order_num')


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
        depth = 1



