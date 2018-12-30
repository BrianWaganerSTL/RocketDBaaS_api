from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from django.db.models import Q

from dbaas import models
from dbaas.models import Cluster, Application, ServerPort, PoolServer, DataCenterChoices, Server


def create_cluster(request):
    if request.method == 'GET':
        poolServers = Server.objects.filter(node_role='PoolServer')
        dataCenterChoicesDict = dict(DataCenterChoices.choices)
        return render(request, 'cluster/create.html',
                      {'servers': poolServers,
                      'dataCenterChoicesDict': dataCenterChoicesDict })


    if request.method == 'POST':
        if request.POST['application_name'] and \
                request.POST['cluster_name'] and \
                request.POST['dbms_type'] and \
                request.POST['cluster_name'] and \
                request.POST['requested_cpu'] and \
                request.POST['requested_ram_gb'] and \
                request.POST['requested_db_gb'] and \
                request.POST['tls_enabled_sw'] and \
                request.POST['backup_retention_days']:

            application = Application()
            try:
                application = get_object_or_404(
                    Application.objects.filter(application_name=request.POST['application_name']))
            except:
                application.application_name = request.POST['application_name']
                application.active_sw = True
                application.save()

            cluster = Cluster()
            cluster.application = application
            cluster.dbms_type = 'PostgreSQL'  # request.POST['dbms_type']
            cluster.cluster_name = request.POST['cluster_name']
            cluster.requested_cpu = request.POST['requested_cpu']
            cluster.requested_ram_gb = request.POST['requested_ram_gb']
            cluster.requested_db_gb = request.POST['requested_db_gb']
            cluster.tls_enabled_sw = request.POST['tls_enabled_sw']
            cluster.backup_retention_days = request.POST['backup_retention_days']
            cluster.active_sw = 'True'

            cluster.cluster_health = Cluster.ClusterHealthChoices.ClusterConfiguring

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

            cluster.environment = models.EnvironmentChoices.SBX
            cluster.save()

            return redirect('cluster_details', cluster.id, )
        else:
            return render(request, 'cluster/create.html', {'error': 'All fields must be filled in'})
    else:
        return render(request, 'cluster/create.html')
