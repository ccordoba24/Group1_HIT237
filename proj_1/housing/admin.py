from django.contrib import admin

from .models import (
    Community,
    Dwelling,
    Tenant,
    Category,
    RepairRequest,
    MaintenanceUpdate
)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region",
    )

    search_fields = (
        "name",
        "region",
    )


@admin.register(Dwelling)
class DwellingAdmin(admin.ModelAdmin):
    list_display = (
        "dwelling_code",
        "address",
        "community",
    )

    search_fields = (
        "dwelling_code",
        "address",
    )

    list_filter = (
        "community",
    )


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "dwelling",
    )

    search_fields = (
        "user__username",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "tenant",
        "dwelling",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "tenant__user__username",
    )

    list_filter = (
        "status",
        "category",
    )

    ordering = (
        "-created_at",
    )


@admin.register(MaintenanceUpdate)
class MaintenanceUpdateAdmin(admin.ModelAdmin):
    list_display = (
        "repair_request",
        "updated_at",
    )

    ordering = (
        "-updated_at",
    )