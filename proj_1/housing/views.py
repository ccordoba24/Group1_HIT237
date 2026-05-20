from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView,
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import RepairRequest
from .forms import RepairRequestForm
from .services import RepairRequestService


# --- Home / Static Pages ---

class HomeView(TemplateView):
    template_name = "housing/home.html"


class RegisterView(TemplateView):
    template_name = "housing/register.html"


class FAQView(TemplateView):
    template_name = "housing/faq.html"


class AboutView(TemplateView):
    template_name = "housing/about.html"


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