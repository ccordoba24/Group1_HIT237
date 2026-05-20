from django import forms
from .models import RepairRequest, MaintenanceUpdate


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = [
            "title",
            "description",
            "status",
            "category",
            "dwelling",
            "tenant",
        ]


class MaintenanceUpdateForm(forms.ModelForm):
    class Meta:
        model = MaintenanceUpdate
        fields = ["note"]