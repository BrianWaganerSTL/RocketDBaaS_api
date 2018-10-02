from django.views.generic import DetailView
from django.contrib.messages.middleware import *

from rest_framework.response import Response
from rest_framework import viewsets, request

from dbaas.models import PoolServer, DbmsTypeChoices
from dbaas.serializers.serializers import LockPoolServers2Serializer


# def LockPoolServers(request, needed_servers='3'):
#     print(request)
#     queryset = PoolServer.objects.all()
#     j = needed_servers
#         # filter(statusInPool__exact=PoolServer.StatusInPoolChoices.Available).\
#         # filter(dbmsType__exact=DbmsTypeChoices.MongoDB)
#         # lockedPoolServers = PoolServer.objects.all()
#         # return Response(lockedPoolServers)
#     serializer_class = LockPoolServers2Serializer(queryset)
#     # return HttpResponse('<h1>Locked {} Servers</h1>'.format(NeededServers))
#     # return render(request,{'lockedPoolServers':lockedPoolServers})
#     return 'hi'

class ClaimPoolServers(viewsets.ModelViewSet):
    #requestedCpus=request.get_queryset()
    # print(requestedCpus)

    # cpu = content_params.get('cpu')
    # ram = request.HttpRequest.content_params.get('cpu')
    # ram = request.HttpRequest.content_params.get('cpu')
    #
    # print(cpu)

    queryset = PoolServer.objects.filter(cpu__exact=2)[:2]
    serializer = LockPoolServers2Serializer(queryset)

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Book.objects.all()
    #     return context

