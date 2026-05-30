from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RepairRequest, MaintenanceUpdate, Tenant


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter tenant dropdown to show only the logged-in user's tenant
        if user and user.is_authenticated:
            try:
                user_tenant = Tenant.objects.get(user=user)
                self.fields['tenant'].queryset = Tenant.objects.filter(user=user)
                self.fields['tenant'].initial = user_tenant
            except Tenant.DoesNotExist:
                # If user has no tenant, show all tenants
                pass


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter tenant dropdown to show only the logged-in user's tenant
        if user and user.is_authenticated:
            try:
                user_tenant = Tenant.objects.get(user=user)
                self.fields['tenant'].queryset = Tenant.objects.filter(user=user)
            except Tenant.DoesNotExist:
                # If user has no tenant, show all tenants
                pass


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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Staff can see all tenants, no filtering needed


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