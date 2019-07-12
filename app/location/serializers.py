from rest_framework import serializers

from location.models import Locality, City


class CitySerializer(serializers.ModelSerializer):
    """Serializer for city objects"""

    class Meta:
        model = City
        fields = ('id', 'name')
        read_only_fields = ('id',)


class LocalitySerializer(serializers.ModelSerializer):
    """Serializer for locality objects"""

    class Meta:
        model = Locality
        fields = ('id', 'name', 'latitude', 'longitude', 'city')
        read_only_fields = ('id',)
