from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

from location.models import Locality, City


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
