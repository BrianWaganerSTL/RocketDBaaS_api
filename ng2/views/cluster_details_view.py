from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from ng2.models2 import Cluster, Server, ApplicationContactsDetailsView
from ng2.serializers.ClusterDetailsSerializer import ClusterDetailsSerializer

def cluster_details(request, _cluster_id):
    clusterDetailsSerializer = ClusterDetailsSerializer
    cluster = get_object_or_404(Cluster, pk=_cluster_id)

    servers = Server.objects.filter(cluster_id__exact=_cluster_id)
    contacts = ApplicationContactsDetailsView.objects.filter(id__exact=cluster.application_id)

    return render(request,
                  'cluster_details.html',
                  {'cluster': cluster, 'servers': servers, 'contacts': contacts })

