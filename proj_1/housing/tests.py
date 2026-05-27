from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Community, Dwelling, Tenant, Category, RepairRequest
from .services import RepairRequestService, PermissionService
from .forms import RepairRequestForm
from .exceptions import UnauthorizedRepairActionError


class RepairRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tenant1",
            password="pass12345"
        )
        self.community = Community.objects.create(
            name="Darwin",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            address="House 1",
            dwelling_code="D001"
        )
        self.tenant = Tenant.objects.create(
            user=self.user,
            dwelling=self.dwelling
        )
        self.category = Category.objects.create(
            name="Plumbing"
        )

    def test_repair_request_is_open_when_not_completed(self):
        request = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            category=self.category,
            created_by=self.user,
            title="Broken tap",
            description="Kitchen tap not working",
            status="pending"
        )

        self.assertTrue(request.is_open())
        self.assertFalse(request.is_completed())


class RepairRequestQuerySetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tenant1",
            password="pass12345"
        )
        self.community = Community.objects.create(
            name="Darwin",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            address="House 1",
            dwelling_code="D001"
        )
        self.tenant = Tenant.objects.create(
            user=self.user,
            dwelling=self.dwelling
        )
        self.category = Category.objects.create(
            name="Plumbing"
        )

        RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            category=self.category,
            created_by=self.user,
            title="Open request",
            description="Open issue",
            status="pending"
        )

        RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            category=self.category,
            created_by=self.user,
            title="Completed request",
            description="Fixed issue",
            status="completed"
        )

    def test_custom_queryset_open_returns_only_non_completed_requests(self):
        self.assertEqual(
            RepairRequest.objects.open().count(),
            1
        )

    def test_custom_queryset_completed_returns_only_completed_requests(self):
        self.assertEqual(
            RepairRequest.objects.completed().count(),
            1
        )

    def test_queryset_annotation_adds_update_count(self):
        request = (
            RepairRequest.objects
            .with_update_count()
            .get(title="Open request")
        )

        self.assertEqual(
            request.update_count,
            0
        )


class RepairRequestServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tenant1",
            password="pass12345"
        )
        self.community = Community.objects.create(
            name="Darwin",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            address="House 1",
            dwelling_code="D001"
        )
        self.tenant = Tenant.objects.create(
            user=self.user,
            dwelling=self.dwelling
        )
        self.category = Category.objects.create(
            name="Plumbing"
        )

    def test_service_creates_repair_request_with_created_by_user(self):
        form = RepairRequestForm(data={
            "dwelling": self.dwelling.id,
            "tenant": self.tenant.id,
            "category": self.category.id,
            "title": "Broken door",
            "description": "Front door damaged",
            "status": "pending",
        })

        self.assertTrue(form.is_valid())

        repair_request = RepairRequestService.create_repair_request(
            form=form,
            user=self.user
        )

        self.assertEqual(
            repair_request.created_by,
            self.user
        )
        self.assertEqual(
            repair_request.title,
            "Broken door"
        )

    def test_service_blocks_anonymous_user(self):
        class AnonymousUser:
            is_authenticated = False

        form = RepairRequestForm(data={
            "dwelling": self.dwelling.id,
            "tenant": self.tenant.id,
            "category": self.category.id,
            "title": "Broken door",
            "description": "Front door damaged",
            "status": "pending",
        })

        self.assertTrue(form.is_valid())

        with self.assertRaises(UnauthorizedRepairActionError):
            RepairRequestService.create_repair_request(
                form=form,
                user=AnonymousUser()
            )


class PermissionServiceTests(TestCase):
    def setUp(self):
        self.normal_user = User.objects.create_user(
            username="normaluser",
            password="pass12345"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="pass12345",
            is_staff=True
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="pass12345"
        )

    def test_staff_or_superuser_check_allows_staff(self):
        self.assertTrue(
            PermissionService.is_staff_or_superuser(self.staff_user)
        )

    def test_staff_or_superuser_check_allows_superuser(self):
        self.assertTrue(
            PermissionService.is_staff_or_superuser(self.admin_user)
        )

    def test_staff_or_superuser_check_blocks_normal_user(self):
        self.assertFalse(
            PermissionService.is_staff_or_superuser(self.normal_user)
        )

    def test_normal_user_cannot_add_maintenance_update(self):
        self.assertFalse(
            PermissionService.can_add_maintenance_update(self.normal_user)
        )

    def test_staff_can_add_maintenance_update(self):
        self.assertTrue(
            PermissionService.can_add_maintenance_update(self.staff_user)
        )


class RepairRequestViewPermissionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tenant1",
            password="pass12345"
        )
        self.other_user = User.objects.create_user(
            username="tenant2",
            password="pass12345"
        )
        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="pass12345",
            is_staff=True
        )

        self.community = Community.objects.create(
            name="Darwin",
            region="NT"
        )
        self.dwelling = Dwelling.objects.create(
            community=self.community,
            address="House 1",
            dwelling_code="D001"
        )
        self.tenant = Tenant.objects.create(
            user=self.user,
            dwelling=self.dwelling
        )
        self.other_tenant = Tenant.objects.create(
            user=self.other_user,
            dwelling=self.dwelling
        )
        self.category = Category.objects.create(
            name="Plumbing"
        )

        self.request_obj = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            category=self.category,
            created_by=self.user,
            title="Broken tap",
            description="Kitchen tap not working",
            status="pending"
        )

        self.staff_created_request_for_tenant = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.tenant,
            category=self.category,
            created_by=self.staff_user,
            title="Staff logged tenant issue",
            description="Staff created this request for tenant1",
            status="pending"
        )

        self.other_user_request = RepairRequest.objects.create(
            dwelling=self.dwelling,
            tenant=self.other_tenant,
            category=self.category,
            created_by=self.other_user,
            title="Other tenant request",
            description="This request belongs to tenant2",
            status="pending"
        )

    def test_create_view_requires_login(self):
        response = self.client.get(
            reverse("repair-request-create")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_owner_can_access_update_view(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "repair-request-update",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_other_user_cannot_access_update_view(self):
        self.client.login(
            username="tenant2",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "repair-request-update",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            404
        )

    def test_staff_can_access_update_view(self):
        self.client.login(
            username="staffuser",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "repair-request-update",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_dashboard_loads_for_logged_in_user(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            "Housing Maintenance Dashboard"
        )

    def test_tenant_can_see_request_linked_to_tenant_profile(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse("repair-request-list")
        )

        self.assertContains(
            response,
            "Broken tap"
        )
        self.assertContains(
            response,
            "Staff logged tenant issue"
        )

    def test_normal_user_cannot_see_unrelated_tenant_request(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse("repair-request-list")
        )

        self.assertNotContains(
            response,
            "Other tenant request"
        )

    def test_normal_user_edit_form_does_not_show_status(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "repair-request-update",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertNotContains(
            response,
            'name="status"'
        )

    def test_staff_edit_form_shows_status(self):
        self.client.login(
            username="staffuser",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "repair-request-update",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )
        self.assertContains(
            response,
            'name="status"'
        )

    def test_normal_user_cannot_access_maintenance_update_page(self):
        self.client.login(
            username="tenant1",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "maintenance-update-create",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_staff_can_access_maintenance_update_page(self):
        self.client.login(
            username="staffuser",
            password="pass12345"
        )

        response = self.client.get(
            reverse(
                "maintenance-update-create",
                args=[self.request_obj.id]
            )
        )

        self.assertEqual(
            response.status_code,
            200
        )