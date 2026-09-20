from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceZoneViewSet,
    SpecializationViewSet,
    StaffAvailabilityViewSet,
    StaffTimeOffViewSet,
    StaffViewSet,
)

router = DefaultRouter()
router.register(r"staff", StaffViewSet, basename="staff")
router.register(r"specializations", SpecializationViewSet, basename="specialization")
router.register(r"service-zones", ServiceZoneViewSet, basename="service-zone")
router.register(r"staff-availability", StaffAvailabilityViewSet, basename="staff-availability")
router.register(r"staff-time-off", StaffTimeOffViewSet, basename="staff-time-off")

urlpatterns = [path("", include(router.urls))]
