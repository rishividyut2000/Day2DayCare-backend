from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PlanExerciseViewSet,
    PlanPhaseViewSet,
    PlanRevisionViewSet,
    ProgressionNoteViewSet,
    TreatmentPlanViewSet,
)

router = DefaultRouter()
router.register(r"treatment-plans", TreatmentPlanViewSet, basename="treatment-plan")
router.register(r"plan-phases", PlanPhaseViewSet, basename="plan-phase")
router.register(r"plan-exercises", PlanExerciseViewSet, basename="plan-exercise")
router.register(r"plan-revisions", PlanRevisionViewSet, basename="plan-revision")
router.register(r"progression-notes", ProgressionNoteViewSet, basename="progression-note")

urlpatterns = [path("", include(router.urls))]
