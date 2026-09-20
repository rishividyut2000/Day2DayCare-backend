from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeviceTokenViewSet, FollowUpViewSet, NotificationLogViewSet, NotificationTemplateViewSet, ReminderViewSet

router = DefaultRouter()
router.register(r"notification-templates", NotificationTemplateViewSet, basename="notification-template")
router.register(r"reminders", ReminderViewSet, basename="reminder")
router.register(r"notification-log", NotificationLogViewSet, basename="notification-log")
router.register(r"follow-ups", FollowUpViewSet, basename="follow-up")
router.register(r"device-tokens", DeviceTokenViewSet, basename="device-token")

urlpatterns = [path("", include(router.urls))]
