from rest_framework import viewsets

from location.models import Locality, City

from location.serializers import LocalitySerializer, CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    """Manage City objects"""
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        return self.queryset


class LocalityViewSet(viewsets.ModelViewSet):
    """Manage locality objects"""
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer

    def get_queryset(self):
        return self.queryset
