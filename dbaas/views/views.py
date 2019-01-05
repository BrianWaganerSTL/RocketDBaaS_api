from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (AllowAny)
from django.http import HttpResponse
from django.shortcuts import render
from dbaas.models import Server
from dbaas.serializers.serializers import LockPoolServersSerializer


def CreateDBInit(request):
    return render(request, "createDB.html", {'obj': CreateDBInit})


def profile(request, NeededServers=3):
   return HttpResponse('<h1>hi username: {}</h1>'.format(NeededServers))


class LockPoolServersViewSet(ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = LockPoolServersSerializer
    permission_classes = [AllowAny,]


    def poolserver_list(self, poolServersNeeded):
        queryset = Server.objects.filter(poolServersNeeded__=poolServersNeeded)
        poolServersQS = self.get_queryset()
        serializer = LockPoolServersSerializer(poolServersQS)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        print(self.request.query_params)
        print(self.lookup_url_kwarg)
        poolServersQS = self.get_queryset()
        serializer = LockPoolServersSerializer(poolServersQS)
        return Response(serializer.data)
