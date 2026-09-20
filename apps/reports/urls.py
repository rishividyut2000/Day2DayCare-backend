from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReportMetricViewSet

router = DefaultRouter()
router.register(r"report-metrics", ReportMetricViewSet, basename="report-metric")

urlpatterns = [path("", include(router.urls))]
