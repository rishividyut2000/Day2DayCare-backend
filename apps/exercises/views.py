"""API views."""

from rest_framework import viewsets

from .models import Exercise, ExerciseCategory, ExerciseMedia
from .serializers import ExerciseCategorySerializer, ExerciseMediaSerializer, ExerciseSerializer


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseCategory.objects.filter(deleted_at__isnull=True)
    serializer_class = ExerciseCategorySerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.filter(deleted_at__isnull=True)
    serializer_class = ExerciseSerializer


class ExerciseMediaViewSet(viewsets.ModelViewSet):
    queryset = ExerciseMedia.objects.filter(deleted_at__isnull=True)
    serializer_class = ExerciseMediaSerializer
