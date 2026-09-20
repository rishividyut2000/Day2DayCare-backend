from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppSettingViewSet,
    BranchHoursViewSet,
    BranchViewSet,
    DisciplineViewSet,
    NumberingSequenceViewSet,
)

router = DefaultRouter()
router.register(r"branches", BranchViewSet, basename="branch")
router.register(r"branch-hours", BranchHoursViewSet, basename="branch-hour")
router.register(r"disciplines", DisciplineViewSet, basename="discipline")
router.register(r"settings", AppSettingViewSet, basename="setting")
router.register(r"numbering-sequences", NumberingSequenceViewSet, basename="numbering-sequence")

urlpatterns = [path("", include(router.urls))]
