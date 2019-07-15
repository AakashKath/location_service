from django.db.models import Q, F, ExpressionWrapper, DecimalField
from rest_framework import viewsets

from location.models import Locality, City

from location.serializers import LocalitySerializer, CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    """Manage City objects"""
    queryset = City.objects.all()
    serializer_class = CitySerializer


class LocalityNameViewSet(viewsets.ModelViewSet):
    """Manage locality objects by name"""
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer

    def get_queryset(self):
        city = self.request.query_params.get('name')
        lat_str = self.request.query_params.get('lat') or '0'
        long_str = self.request.query_params.get('long') or '0'
        lat = float(lat_str)
        long = float(long_str)
        queryset = self.queryset
        if city:
            queryset = queryset.filter(name__istartswith=city).order_by((F('latitude')-lat)**2+(F('longitude')-long)**2)[:5]

        return queryset


class LocalityDistanceViewSet(viewsets.ModelViewSet):
    """Manage locality objects by distance"""
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer

    def get_queryset(self):
        lat_str = self.request.query_params.get('lat') or '0'
        long_str = self.request.query_params.get('long') or '0'
        lat = float(lat_str)
        long = float(long_str)
        queryset = self.queryset
        if lat_str and long_str:
            queryset=queryset.annotate(distance=(F('latitude')-lat)**2+(F('longitude')-long)**2).filter(distance__lte=10).order_by((F('latitude')-lat)**2+(F('longitude')-long)**2)

        return queryset
    
