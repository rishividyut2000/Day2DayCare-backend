"""URLs served inside a tenant schema — the clinic-facing API."""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_v1 = [
    path("auth/", include("apps.accounts.urls")),
    path("", include("apps.branches.urls")),
    path("", include("apps.staff.urls")),
    path("", include("apps.patients.urls")),
    path("", include("apps.referrals.urls")),
    path("", include("apps.clinical.urls")),
    path("", include("apps.exercises.urls")),
    path("", include("apps.plans.urls")),
    path("", include("apps.scheduling.urls")),
    path("", include("apps.billing.urls")),
    path("", include("apps.notifications.urls")),
    path("", include("apps.reports.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(api_v1)),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("health/", include("apps.common.urls")),
]
