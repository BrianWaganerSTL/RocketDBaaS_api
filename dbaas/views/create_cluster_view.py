from django.core.exceptions import FieldError
from django.db import IntegrityError
from django.db.models import FieldDoesNotExist
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework.utils import json

from dbaas.models import Cluster, Application, ServerPort, Environment


@csrf_exempt
def create_cluster(request):
    if request.method == 'POST':
        post_json = json.loads(request.body)

        application = Application()
        application_name = post_json.get("application_name")
        try:
            application = get_object_or_404(
                Application.objects.filter(application_name=application_name))
        except (FieldDoesNotExist, FieldError, IntegrityError, TypeError, ValueError) as ex:
            print('Error: ' + str(ex))
            # No Application found, make a new one
            application.application_name = application_name
            application.active_sw = True
            application.save()

        environment = Environment()
        environment = get_object_or_404(Environment.objects.filter(env_name=post_json.get("environment")))
        print('env = ' + str(environment.env_name))


        cluster = Cluster()
        cluster.application = application
        cluster.dbms_type = post_json.get('dbms_type')
        cluster.cluster_name = post_json.get('cluster_name')
        cluster.tls_enabled_sw = post_json.get('tls_enabled_sw')
        cluster.backup_retention_days = post_json.get('backup_retention_days')
        cluster.active_sw = 'True'
        print('flag2')
        cluster.cluster_health = post_json.get('cluster_health')

        print('flag3')
        nextOpenPort = ServerPort().NextOpenPort()
        print('RW nextOpenPort=' + str(nextOpenPort))
        read_write_port = get_object_or_404(ServerPort.objects.filter(port=nextOpenPort))
        read_write_port.port_status = ServerPort.PortStatusChoices.Locked
        read_write_port.port_notes = 'R/W for ' + cluster.cluster_name
        read_write_port.save()
        cluster.read_write_port = read_write_port

        nextOpenPort = ServerPort().NextOpenPort()
        print('RO nextOpenPort=' + str(nextOpenPort))
        read_only_port = get_object_or_404(ServerPort.objects.filter(port=nextOpenPort))
        read_only_port.port_status = ServerPort.PortStatusChoices.Locked
        read_only_port.port_notes = 'R/O for ' + cluster.cluster_name
        read_only_port.save()
        cluster.read_only_port = read_only_port

        cluster.environment = environment
        cluster.save()
        print('Cluster Saved')

        return redirect('cluster_details', cluster.id, )
