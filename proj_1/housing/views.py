from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import RepairRequest, MaintenanceUpdate
from .forms import (
    RepairRequestCreateForm,
    RepairRequestUserUpdateForm,
    RepairRequestStaffUpdateForm,
    MaintenanceUpdateForm,
    UserRegisterForm,
)
from .services import RepairRequestService, PermissionService


# --- Home / Static Pages ---

class HomeView(TemplateView):
    template_name = "housing/home.html"


# --- Authentication Views ---

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "housing/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    template_name = "housing/login.html"

    def get_success_url(self):
        return reverse_lazy("dashboard")


# --- Shared Permission Query Helper ---

class RepairRequestAccessMixin:
    def get_accessible_requests(self):
        if PermissionService.is_staff_or_superuser(self.request.user):
            return RepairRequest.objects.all()

        return RepairRequest.objects.filter(
            Q(created_by=self.request.user) |
            Q(tenant__user=self.request.user)
        ).distinct()


# --- Dashboard ---

class DashboardView(LoginRequiredMixin, RepairRequestAccessMixin, TemplateView):
    template_name = "housing/dashboard.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        requests = self.get_accessible_requests()

        context["total_requests"] = requests.count()
        context["open_requests"] = requests.open().count()
        context["completed_requests"] = requests.completed().count()

        context["requests_by_status"] = (
            requests
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )

        return context


# --- Repair Request List ---

class RepairRequestListView(LoginRequiredMixin, RepairRequestAccessMixin, ListView):
    model = RepairRequest
    template_name = "housing/repair_request_list.html"
    context_object_name = "requests"
    login_url = "/login/"

    def get_queryset(self):
        return (
            self.get_accessible_requests()
            .select_related(
                "category",
                "dwelling",
                "tenant__user"
            )
            .prefetch_related("updates")
            .with_update_count()
            .order_by("-created_at")
        )


# --- Repair Request Detail ---

class RepairRequestDetailView(LoginRequiredMixin, RepairRequestAccessMixin, DetailView):
    model = RepairRequest
    template_name = "housing/repair_request_detail.html"
    context_object_name = "request"
    login_url = "/login/"

    def get_queryset(self):
        return (
            self.get_accessible_requests()
            .select_related(
                "category",
                "dwelling",
                "tenant__user"
            )
            .prefetch_related("updates")
        )


# --- Create Request ---

class RepairRequestCreateView(LoginRequiredMixin, CreateView):
    model = RepairRequest
    form_class = RepairRequestCreateForm
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")
    login_url = "/login/"

    def form_valid(self, form):
        self.object = RepairRequestService.create_repair_request(
            form=form,
            user=self.request.user
        )
        return super().form_valid(form)


# --- Update Request ---

class RepairRequestUpdateView(LoginRequiredMixin, RepairRequestAccessMixin, UpdateView):
    model = RepairRequest
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")
    login_url = "/login/"

    def get_queryset(self):
        return self.get_accessible_requests()

    def get_form_class(self):
        if PermissionService.is_staff_or_superuser(self.request.user):
            return RepairRequestStaffUpdateForm

        return RepairRequestUserUpdateForm

    def form_valid(self, form):
        self.object = RepairRequestService.update_repair_request(
            form=form,
            user=self.request.user
        )
        return super().form_valid(form)


# --- Maintenance History ---

class MaintenanceHistoryView(LoginRequiredMixin, RepairRequestAccessMixin, ListView):
    model = RepairRequest
    template_name = "housing/maintenance_history.html"
    context_object_name = "completed_requests"
    login_url = "/login/"

    def get_queryset(self):
        return (
            self.get_accessible_requests()
            .completed()
            .with_update_count()
            .order_by("-updated_at")
        )


# --- Add Maintenance Update ---

class MaintenanceUpdateCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceUpdate
    form_class = MaintenanceUpdateForm
    template_name = "housing/maintenance_update_form.html"
    login_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        if not PermissionService.can_add_maintenance_update(request.user):
            return HttpResponseForbidden(
                "Only staff or admin users can add maintenance updates."
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        repair_request = RepairRequest.objects.get(pk=self.kwargs["pk"])
        form.instance.repair_request = repair_request
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "repair-request-detail",
            kwargs={"pk": self.kwargs["pk"]}
        )