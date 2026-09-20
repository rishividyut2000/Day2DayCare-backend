from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentStatusHistoryViewSet,
    AppointmentViewSet,
    FeedbackViewSet,
    HomeVisitLogViewSet,
    HomeVisitViewSet,
    ModalityViewSet,
    SessionModalityViewSet,
    SessionViewSet,
    ServiceTypeViewSet,
)

router = DefaultRouter()
router.register(r"service-types", ServiceTypeViewSet, basename="service-type")
router.register(r"appointments", AppointmentViewSet, basename="appointment")
router.register(r"appointment-status-history", AppointmentStatusHistoryViewSet, basename="appointment-status-history")
router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"modalities", ModalityViewSet, basename="modality")
router.register(r"session-modalities", SessionModalityViewSet, basename="session-modality")
router.register(r"home-visits", HomeVisitViewSet, basename="home-visit")
router.register(r"home-visit-logs", HomeVisitLogViewSet, basename="home-visit-log")
router.register(r"feedback", FeedbackViewSet, basename="feedback")

urlpatterns = [path("", include(router.urls))]
