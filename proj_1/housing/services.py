from django.db import transaction

from .exceptions import InvalidRepairRequestError, UnauthorizedRepairActionError
from .models import RepairRequest


class RepairRequestService:
    @staticmethod
    @transaction.atomic
    def create_repair_request(form, user):
        if not user.is_authenticated:
            raise UnauthorizedRepairActionError("User must be logged in to create a repair request.")

        repair_request = form.save(commit=False)
        repair_request.created_by = user

        if not repair_request.title:
            raise InvalidRepairRequestError("Repair request title is required.")

        repair_request.save()
        form.save_m2m()
        return repair_request

    @staticmethod
    @transaction.atomic
    def update_repair_request(form, user):
        if not user.is_authenticated:
            raise UnauthorizedRepairActionError("User must be logged in to update a repair request.")

        repair_request = form.save(commit=False)

        if not repair_request.title:
            raise InvalidRepairRequestError("Repair request title is required.")

        repair_request.save()
        form.save_m2m()
        return repair_request