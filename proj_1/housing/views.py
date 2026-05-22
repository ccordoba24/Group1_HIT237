from django.db.models import Count
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
from .forms import RepairRequestForm, MaintenanceUpdateForm
from .services import RepairRequestService, PermissionService


# --- Home / Static Pages ---

class HomeView(TemplateView):
    template_name = "housing/home.html"


class RegisterView(TemplateView):
    template_name = "housing/register.html"


class FAQView(TemplateView):
    template_name = "housing/faq.html"


class AboutView(TemplateView):
    template_name = "housing/about.html"


# --- Dashboard ---

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "housing/dashboard.html"
    login_url = "/admin/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_requests"] = RepairRequest.objects.count()
        context["open_requests"] = RepairRequest.objects.open().count()
        context["completed_requests"] = RepairRequest.objects.completed().count()

        context["requests_by_status"] = (
            RepairRequest.objects
            .values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )

        return context


# --- Repair Request List ---

class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repair_request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        return (
            RepairRequest.objects
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

class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/repair_request_detail.html"
    context_object_name = "request"

    def get_queryset(self):
        return (
            RepairRequest.objects
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
    form_class = RepairRequestForm
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")
    login_url = "/admin/login/"

    def form_valid(self, form):
        self.object = RepairRequestService.create_repair_request(
            form=form,
            user=self.request.user
        )
        return super().form_valid(form)


# --- Update Request ---

class RepairRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")
    login_url = "/admin/login/"

    def get_queryset(self):
        if PermissionService.is_staff_or_superuser(self.request.user):
            return RepairRequest.objects.all()

        return RepairRequest.objects.filter(
            created_by=self.request.user
        )

    def form_valid(self, form):
        self.object = RepairRequestService.update_repair_request(
            form=form,
            user=self.request.user
        )
        return super().form_valid(form)


# --- Maintenance History ---

class MaintenanceHistoryView(ListView):
    model = RepairRequest
    template_name = "housing/maintenance_history.html"
    context_object_name = "completed_requests"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .completed()
            .with_update_count()
            .order_by("-updated_at")
        )


# --- Add Maintenance Update ---

class MaintenanceUpdateCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceUpdate
    form_class = MaintenanceUpdateForm
    template_name = "housing/maintenance_update_form.html"
    login_url = "/admin/login/"

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