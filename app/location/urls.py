from django.urls import path, include
from rest_framework.routers import DefaultRouter

from location import views


router = DefaultRouter()

router.register('city', views.CityViewSet)
router.register(
    'locality-name',
    views.LocalityNameViewSet,
    base_name='locality-name'
)
router.register(
    'locality-distance',
    views.LocalityDistanceViewSet,
    base_name='locality-distance'
)

app_name = 'location'

urlpatterns = [
    path('', include(router.urls)),
]
