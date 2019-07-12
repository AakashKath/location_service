from django.db import models


class City(models.Model):
    """City object"""
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Locality(models.Model):
    """Locality object"""
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    longitude = models.DecimalField(max_digits=8, decimal_places=6)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
