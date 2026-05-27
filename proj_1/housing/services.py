from django.db import transaction

from .exceptions import InvalidRepairRequestError, UnauthorizedRepairActionError
from .models import RepairRequest


class PermissionService:
    @staticmethod
    def is_staff_or_superuser(user):
        return (
            user.is_authenticated
            and (
                user.is_staff
                or user.is_superuser
            )
        )

    @staticmethod
    def can_update_repair_request(user, repair_request):
        if not user.is_authenticated:
            return False

        if PermissionService.is_staff_or_superuser(user):
            return True

        if repair_request.created_by == user:
            return True

        if repair_request.tenant and repair_request.tenant.user == user:
            return True

        return False

    @staticmethod
    def can_add_maintenance_update(user):
        return PermissionService.is_staff_or_superuser(user)


class RepairRequestService:
    @staticmethod
    @transaction.atomic
    def create_repair_request(form, user):
        if not user.is_authenticated:
            raise UnauthorizedRepairActionError(
                "User must be logged in to create a repair request."
            )

        repair_request = form.save(commit=False)
        repair_request.created_by = user

        if not repair_request.title:
            raise InvalidRepairRequestError(
                "Repair request title is required."
            )

        repair_request.save()
        form.save_m2m()
        return repair_request

    @staticmethod
    @transaction.atomic
    def update_repair_request(form, user):
        if not user.is_authenticated:
            raise UnauthorizedRepairActionError(
                "User must be logged in to update a repair request."
            )

        repair_request = form.save(commit=False)

        if not PermissionService.can_update_repair_request(
            user,
            repair_request
        ):
            raise UnauthorizedRepairActionError(
                "User is not allowed to update this repair request."
            )

        if not repair_request.title:
            raise InvalidRepairRequestError(
                "Repair request title is required."
            )

        repair_request.save()
        form.save_m2m()
        return repair_request