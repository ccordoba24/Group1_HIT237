from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]