from rest_framework.routers import DefaultRouter
from tax_payments.api import viewsets

router = DefaultRouter()
router.register("tax", viewsets.TaxViewSet, "tax")
router.register("tax_payment", viewsets.TaxPaymentViewSet, "tax_payments")
urlpatterns = router.urls
