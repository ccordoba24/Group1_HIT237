from django.urls import path
from .views import RepairRequestListView

urlpatterns = [
    path("requests/", RepairRequestListView.as_view(), name="repair-request-list"),
]