from django.views.generic import ListView, DetailView, CreateView, UpdateView,TemplateView
from django.urls import reverse_lazy
from .models import RepairRequest
from .forms import RepairRequestForm
# --- Habiba: Home View ---
class HomeView(TemplateView):
    template_name = "housing/home.html"
class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repair_request_list.html"
    context_object_name = "requests"


class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/repair_request_detail.html"
    context_object_name = "request"


class RepairRequestCreateView(CreateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")


class RepairRequestUpdateView(UpdateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = "housing/repair_request_form.html"
    success_url = reverse_lazy("repair-request-list")

# --- Habiba: Maintenance History View ---
class MaintenanceHistoryView(ListView):
    model = RepairRequest
    template_name = "housing/maintenance_history.html"
    context_object_name = "completed_requests"
 
    def get_queryset(self):
        return RepairRequest.objects.filter(status="completed").order_by("-updated_at")