from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from location.models import Locality, City

from location.serializers import LocalitySerializer, CitySerializer

LOCATION_URL = reverse('location:locality-list')
CITY_URL = reverse('location:city-list')


def sample_city(name='city'):
    """Creates and returns sample city"""
    return City.objects.create(name=name)


def sample_locality(**params):
    """Creates and returns sample locality"""
    defaults = {
        'name': 'local',
        'latitude': 0,
        'longitude': 0,
        'city': sample_city()
    }
    defaults.update(params)

    return Locality.objects.create(**defaults)


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
        city = sample_city(name='city1')

        self.assertEqual(str(city), city.name)

    def test_locality_str(self):
        """Test city string representation"""
        locality = sample_locality(name='local1')

        self.assertEqual(str(locality), locality.name)


class LocalityApiTests(TestCase):
    """Test Locality API"""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_locality(self):
        """Test retrieving localities"""
        sample_locality(name='local2')
        sample_locality(name='local1')
        res = self.client.get(LOCATION_URL)

        locality = Locality.objects.all().order_by('-name')
        serializer = LocalitySerializer(locality, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_locality_successful(self):
        """Test creating a new locality"""
        city1 = sample_city(name='city1')
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
        city1 = sample_city(name='city1')
        payload = {
            'name': '',
            'latitude': 28.466591,
            'longitude': 77.033310,
            'city': city1.id
        }
        res = self.client.post(LOCATION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_in_city_name(self):
        """Test search for top 2 cities"""
        city1 = sample_city(name='gurugram')
        city2 = sample_city(name='jaipur')
        city3 = sample_city(name='delhi')
        city4 = sample_city(name='bangalore')

        res = self.client.get(CITY_URL, {'name': 'guru'})

        serializer1 = CitySerializer(city1)
        serializer2 = CitySerializer(city2)
        serializer3 = CitySerializer(city3)
        serializer4 = CitySerializer(city4)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
        self.assertNotIn(serializer4.data, res.data)

    # def test_search_alphabetically_top_locality(self):
    #     """Test search for top 2 localities"""
    #     sample_locality(name='badshahpur')
    #     sample_locality(name='mgroad')
    #     sample_locality(name='iffco')
    #     sample_locality(name='southex')

    #     res = self.client.get(LOCATION_URL)
