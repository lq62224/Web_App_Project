from rest_framework.decorators import api_view

from rest_framework.response import Response
from base.models import Client
from .serializers import ClientSerializer
from base.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/clients',
        'GET /api/clients/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getClients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getClient(request, pk):
    client = Client.objects.get(id=pk)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)