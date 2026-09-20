from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AssessmentDiagnosisViewSet,
    AssessmentPainViewSet,
    AssessmentRomViewSet,
    AssessmentStrengthViewSet,
    AssessmentViewSet,
    BodyRegionViewSet,
    DiagnosisMasterViewSet,
    EpisodeViewSet,
    JointViewSet,
    MedicalHistoryViewSet,
)

router = DefaultRouter()
router.register(r"episodes", EpisodeViewSet, basename="episode")
router.register(r"medical-history", MedicalHistoryViewSet, basename="medical-history")
router.register(r"body-regions", BodyRegionViewSet, basename="body-region")
router.register(r"joints", JointViewSet, basename="joint")
router.register(r"diagnosis-master", DiagnosisMasterViewSet, basename="diagnosis-master")
router.register(r"assessments", AssessmentViewSet, basename="assessment")
router.register(r"assessment-pain", AssessmentPainViewSet, basename="assessment-pain")
router.register(r"assessment-rom", AssessmentRomViewSet, basename="assessment-rom")
router.register(r"assessment-strength", AssessmentStrengthViewSet, basename="assessment-strength")
router.register(r"assessment-diagnoses", AssessmentDiagnosisViewSet, basename="assessment-diagnosis")

urlpatterns = [path("", include(router.urls))]
