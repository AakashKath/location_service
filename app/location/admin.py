from django.contrib import admin

from location import models


admin.site.register(models.City)
admin.site.register(models.Locality)
