from django.db import models
from django.contrib.auth.models import User


class Community(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.region})"


class Dwelling(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    dwelling_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.address} [{self.dwelling_code}]"

    def open_requests_count(self):
        return self.repairrequest_set.exclude(status="completed").count()


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dwelling = models.ForeignKey(Dwelling, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RepairRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    dwelling = models.ForeignKey(Dwelling, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def is_open(self):
        return self.status != "completed"

    def is_completed(self):
        return self.status == "completed"


class MaintenanceUpdate(models.Model):
    repair_request = models.ForeignKey(
        RepairRequest,
        on_delete=models.CASCADE,
        related_name="updates"
    )
    note = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Update for {self.repair_request.title} at {self.updated_at:%Y-%m-%d %H:%M}"