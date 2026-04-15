from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from housing.models import Community, Dwelling, Tenant, Category, RepairRequest


class Command(BaseCommand):
    help = "Seed demo data for the housing project"

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username="adminfinal").exists():
            User.objects.create_superuser(
                username="adminfinal",
                email="admin@example.com",
                password="Admin12345"
            )
            self.stdout.write(self.style.SUCCESS("Created superuser: adminfinal"))
        else:
            self.stdout.write("Superuser adminfinal already exists")

        test_user, created = User.objects.get_or_create(username="testuser")
        if created:
            test_user.set_password("Test12345")
            test_user.save()
            self.stdout.write(self.style.SUCCESS("Created test user: testuser"))
        else:
            self.stdout.write("Test user already exists")

        category, _ = Category.objects.get_or_create(name="Plumbing")

        community, _ = Community.objects.get_or_create(
            name="Darwin",
            defaults={"region": "NT"}
        )

        dwelling, _ = Dwelling.objects.get_or_create(
            dwelling_code="D001",
            defaults={
                "community": community,
                "address": "House 1"
            }
        )

        tenant, _ = Tenant.objects.get_or_create(
            user=test_user,
            defaults={"dwelling": dwelling}
        )

        repair_request, created = RepairRequest.objects.get_or_create(
            title="Broken tap",
            defaults={
                "description": "Kitchen tap not working",
                "status": "pending",
                "category": category,
                "dwelling": dwelling,
                "tenant": tenant,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS("Created sample repair request"))
        else:
            self.stdout.write("Sample repair request already exists")

        self.stdout.write(self.style.SUCCESS("Demo data setup complete"))