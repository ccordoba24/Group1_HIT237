from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    DashboardView,
    UserLoginView,
    RepairRequestListView,
    RepairRequestDetailView,
    RepairRequestCreateView,
    RepairRequestUpdateView,
    MaintenanceHistoryView,
    MaintenanceUpdateCreateView,
    HomeView,
    RegisterView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path(
        "login/",
        UserLoginView.as_view(),
        name="login"
    ),

    path(
        "logout/",
        LogoutView.as_view(next_page="login"),
        name="logout"
    ),

    path(
        "dashboard/",
        DashboardView.as_view(),
        name="dashboard"
    ),

    path(
        "requests/",
        RepairRequestListView.as_view(),
        name="repair-request-list"
    ),

    path(
        "requests/new/",
        RepairRequestCreateView.as_view(),
        name="repair-request-create"
    ),

    path(
        "requests/<int:pk>/",
        RepairRequestDetailView.as_view(),
        name="repair-request-detail"
    ),

    path(
        "requests/<int:pk>/edit/",
        RepairRequestUpdateView.as_view(),
        name="repair-request-update"
    ),

    path(
        "requests/<int:pk>/update/",
        MaintenanceUpdateCreateView.as_view(),
        name="maintenance-update-create"
    ),

    path(
        "history/",
        MaintenanceHistoryView.as_view(),
        name="maintenance-history"
    ),

    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),
]