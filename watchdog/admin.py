from django.contrib import admin

from .models import Service

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    exclude = ['last_failed', 'recovered', 'prechecked', 'failure', 'downtime']