from django.urls import path
from .views import (
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    MaintenanceHistoryView,
    HomeView
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("requests/", RepairRequestListView.as_view(), name="repair-request-list"),
    path("requests/new/", RepairRequestCreateView.as_view(), name="repair-request-create"),
    path("requests/<int:pk>/", RepairRequestDetailView.as_view(), name="repair-request-detail"),
    path("requests/<int:pk>/edit/", RepairRequestUpdateView.as_view(), name="repair-request-update"),
    # --- Habiba: Maintenance History URL ---
    path("history/", MaintenanceHistoryView.as_view(), name="maintenance-history"),
]