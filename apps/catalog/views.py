"""API views."""

from rest_framework import viewsets

from .models import ExerciseMaster, ExerciseMasterMedia
from .serializers import ExerciseMasterMediaSerializer, ExerciseMasterSerializer


class ExerciseMasterViewSet(viewsets.ModelViewSet):
    queryset = ExerciseMaster.objects.filter(deleted_at__isnull=True)
    serializer_class = ExerciseMasterSerializer


class ExerciseMasterMediaViewSet(viewsets.ModelViewSet):
    queryset = ExerciseMasterMedia.objects.filter(deleted_at__isnull=True)
    serializer_class = ExerciseMasterMediaSerializer
