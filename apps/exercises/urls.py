from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExerciseCategoryViewSet, ExerciseMediaViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r"exercise-categories", ExerciseCategoryViewSet, basename="exercise-category")
router.register(r"exercises", ExerciseViewSet, basename="exercise")
router.register(r"exercise-media", ExerciseMediaViewSet, basename="exercise-media")

urlpatterns = [path("", include(router.urls))]
