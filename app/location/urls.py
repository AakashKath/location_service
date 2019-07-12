from django.urls import path, include
from rest_framework.routers import DefaultRouter

from location import views


router = DefaultRouter()
router.register('locality', views.LocalityViewSet)
router.register('city', views.CityViewSet)

app_name = 'location'

urlpatterns = [
    path('', include(router.urls)),
]
