from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from housing.models import Community, Dwelling, Tenant, Category, RepairRequest


class Command(BaseCommand):
    help = "Seed demo data for the housing project"

    def handle(self, *args, **kwargs):

        # Create or reset admin user

        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            }
        )

        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password("Admin12345")
        admin_user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created admin user: admin"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Reset admin password: admin"
                )
            )

        # Create or reset test user

        test_user, created = User.objects.get_or_create(
            username="testuser"
        )

        test_user.set_password("pralin206407")
        test_user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created test user: testuser"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Reset test user password"
                )
            )

        # Create category

        category, _ = Category.objects.get_or_create(
            name="Plumbing"
        )

        # Create community

        community, _ = Community.objects.get_or_create(
            name="Darwin",
            defaults={
                "region": "NT"
            }
        )

        # Create dwelling

        dwelling, _ = Dwelling.objects.get_or_create(
            dwelling_code="D001",
            defaults={
                "community": community,
                "address": "House 1"
            }
        )

        # Create tenant

        tenant, _ = Tenant.objects.get_or_create(
            user=test_user,
            defaults={
                "dwelling": dwelling
            }
        )

        # Create repair request

        repair_request, created = RepairRequest.objects.get_or_create(
            title="Broken tap",
            defaults={
                "description": "Kitchen tap not working",
                "status": "pending",
                "category": category,
                "dwelling": dwelling,
                "tenant": tenant,
                "created_by": admin_user,
            }
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created sample repair request"
                )
            )
        else:
            self.stdout.write(
                "Sample repair request already exists"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data setup complete"
            )
        )