from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvoiceItemViewSet, InvoiceViewSet, PackageViewSet, PatientPackageViewSet, PaymentViewSet, RefundViewSet

router = DefaultRouter()
router.register(r"packages", PackageViewSet, basename="package")
router.register(r"patient-packages", PatientPackageViewSet, basename="patient-package")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"invoice-items", InvoiceItemViewSet, basename="invoice-item")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"refunds", RefundViewSet, basename="refund")

urlpatterns = [path("", include(router.urls))]
