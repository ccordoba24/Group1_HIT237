from django.contrib import admin
from .models import Community, Dwelling, Tenant, Category, RepairRequest, MaintenanceUpdate

admin.site.register(Community)
admin.site.register(Dwelling)
admin.site.register(Tenant)
admin.site.register(Category)
admin.site.register(RepairRequest)
admin.site.register(MaintenanceUpdate)