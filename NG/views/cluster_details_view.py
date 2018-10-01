from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from ng.models import Cluster, Server, Application, ApplicationContact, Contact, ApplicationContactsDetailsView
from ng.serializers.ClusterDetailsSerializer import ClusterDetailsSerializer

def cluster_details(request, _cluster_id):
    clusterDetailsSerializer = ClusterDetailsSerializer
    cluster = get_object_or_404(Cluster, pk=_cluster_id)

    #cluster = Cluster.objects.filter(cluster_name=my_cluster_name).values('id','cluster_name', 'application__application_name')
    servers = Server.objects.filter(cluster_id__exact=_cluster_id)
    contacts = ApplicationContactsDetailsView.objects.filter(id__exact=cluster.application_id)
    #contacts = ApplicationContact.objects.filter(, _cluster_id)
   # contacts = ApplicationContact.objects.filter(application__exact=cluster
    #=cluster.application.application_id).filter(active_sw__exact=True)


    return render(request,
                  'cluster_details.html',
                  {'cluster': cluster, 'servers': servers, 'contacts': contacts })

