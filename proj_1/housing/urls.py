from django.urls import path
from .views import RepairRequestListView, RepairRequestDetailView, RepairRequestCreateView

urlpatterns = [
    path("requests/", RepairRequestListView.as_view(), name="repair-request-list"),
    path("requests/<int:pk>/", RepairRequestDetailView.as_view(), name="repair-request-detail"),
    path("requests/new/", RepairRequestCreateView.as_view(), name="repair-request-create"),
]