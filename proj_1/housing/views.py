from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import RepairRequest
from .forms import RepairRequestForm


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