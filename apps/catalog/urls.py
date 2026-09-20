from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExerciseMasterMediaViewSet, ExerciseMasterViewSet

router = DefaultRouter()
router.register(r"exercise-master", ExerciseMasterViewSet, basename="exercise-master")
router.register(r"exercise-master-media", ExerciseMasterMediaViewSet, basename="exercise-master-media")

urlpatterns = [path("", include(router.urls))]
