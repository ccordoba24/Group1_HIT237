from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import RepairRequest
from .forms import RepairRequestForm


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repair_request_list.html"
    context_object_name = "requests"

    def get_queryset(self):
        return (
            RepairRequest.objects
            .select_related("category", "dwelling", "tenant__user")
            .order_by("-created_at")
        )


class RepairRequestDetailView(DetailView):
    model = RepairRequest
    template_name = "housing/repair_request_detail.html"
    context_object_name = "request"

    def get_queryset(self):
        return RepairRequest.objects.select_related(
            "category", "dwelling", "tenant__user"
        )


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