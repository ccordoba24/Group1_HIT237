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

        # Create categories

        categories_to_create = [
            "Electrical",
            "Plumbing",
            "Fittings",
            "Windows and Doors",
            "Locksmith",
            "Roofing",
            "Walls and Ceilings",
            "Other",
        ]

        for category_name in categories_to_create:
            Category.objects.get_or_create(name=category_name)

        # Get Plumbing category for the sample repair request
        category = Category.objects.get(name="Plumbing")

        # Create community

        community, _ = Community.objects.get_or_create(
            name="Darwin",
            defaults={
                "region": "NT"
            }
        )

        # Create multiple dwellings with different types
        dwelling_data = [
            {"code": "D001", "address": "House 1", "type": "house"},
            {"code": "D002", "address": "House 2", "type": "unit"},
            {"code": "D003", "address": "House 3", "type": "town_house"},
            {"code": "D004", "address": "House 4", "type": "granny_flat"},
            {"code": "D005", "address": "House 5", "type": "room"},
        ]

        for data in dwelling_data:
            Dwelling.objects.get_or_create(
                dwelling_code=data["code"],
                defaults={
                    "community": community,
                    "address": data["address"],
                    "dwelling_type": data["type"],
                }
            )

        # Get the first dwelling (House) for the sample repair request
        dwelling = Dwelling.objects.get(dwelling_code="D001")
        
        # Clean up any 'test' dwellings
        Dwelling.objects.filter(address__icontains="test").delete()

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