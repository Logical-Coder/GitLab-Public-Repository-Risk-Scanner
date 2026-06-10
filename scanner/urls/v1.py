from django.urls import path
from scanner.views import HealthView, ScanView

urlpatterns = [
    path(
        "scan/",
        ScanView.as_view(),
        name="scan"
    ),
    path(
        "health/",
        HealthView.as_view()
    )
    
]