from django.views.generic import ListView
from .models import RepairRequest


class RepairRequestListView(ListView):
    model = RepairRequest
    template_name = "housing/repair_request_list.html"
    context_object_name = "requests"