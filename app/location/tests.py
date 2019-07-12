from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from location.models import Locality, City

from location.serializers import LocalitySerializer

LOCATION_URL = reverse('location:locality-list')
# CITY_URL = reverse('location:city-list')


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)


class ModelTests(TestCase):

    def tes_city_str(self):
        """Test city string representation"""
        city = City.objects.create(name='city1')

        self.assertEqual(str(city), city.name)

    def test_locality_str(self):
        """Test city string representation"""
        city = City.objects.create(name='city1')
        locality = Locality.objects.create(
            name='local1',
            latitude=28.466591,
            longitude=77.033310,
            city=city
        )

        self.assertEqual(str(locality), locality.name)


class LocalityApiTests(TestCase):
    """Test Locality API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_locality(self):
        """Test retrieving localities"""
        city1 = City.objects.create(name='city1')
        Locality.objects.create(
            name='local2',
            latitude=28.466591,
            longitude=77.033310,
            city=city1
        )
        Locality.objects.create(
            name='local1',
            latitude=28.466591,
            longitude=77.033310,
            city=city1
        )
        res = self.client.get(LOCATION_URL)

        locality = Locality.objects.all().order_by('-name')
        serializer = LocalitySerializer(locality, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_locality_successful(self):
        """Test creating a new locality"""
        city1 = City.objects.create(name='city1')
        payload = {
            'name': 'local1',
            'latitude': 28.466591,
            'longitude': 77.033310,
            'city': city1.id
        }
        self.client.post(LOCATION_URL, payload)

        exists = Locality.objects.filter(
            name=payload['name'],
            latitude=payload['latitude'],
            longitude=payload['longitude'],
            city=payload['city']
        ).exists()
        self.assertTrue(exists)

    def test_create_locality_invalid(self):
        """Test creating an invalid locality"""
        city1 = City.objects.create(name='city1')
        payload = {
            'name': '',
            'latitude': 28.466591,
            'longitude': 77.033310,
            'city': city1.id
        }
        res = self.client.post(LOCATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
