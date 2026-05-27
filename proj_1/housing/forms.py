from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RepairRequest, MaintenanceUpdate


class RepairRequestCreateForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = [
            "title",
            "description",
            "category",
            "dwelling",
            "tenant",
        ]


class RepairRequestUserUpdateForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = [
            "title",
            "description",
            "category",
            "dwelling",
            "tenant",
        ]


class RepairRequestStaffUpdateForm(forms.ModelForm):
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
        exclude = [
            "repair_request",
        ]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]


# Backward-compatible aliases for existing tests and older code references.
RepairRequestForm = RepairRequestStaffUpdateForm
RepairRequestUpdateForm = RepairRequestStaffUpdateForm