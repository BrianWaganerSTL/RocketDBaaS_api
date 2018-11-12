from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from dbaas.models import Cluster, Server, ApplicationContactsView, ServerActivity
from dbaas.serializers.ClusterDetailsSerializer import ClusterDetailsSerializer

def cluster_details(request, _cluster_id):
    clusterDetailsSerializer = ClusterDetailsSerializer
    cluster = get_object_or_404(Cluster, pk=_cluster_id)

    servers = Server.objects.filter(cluster_id__exact=_cluster_id)
    contacts = ApplicationContactsView.objects.filter(application_id__exact=cluster.application_id)
    server_activities = ServerActivity.objects.filter(server__cluster_id__exact=_cluster_id)

    return render(request,
                  'cluster_details.html',
                  {'cluster': cluster,
                   'servers': servers,
                   'contacts': contacts,
                   'server_activities': server_activities })

