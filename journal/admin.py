from django.contrib import admin

# Register your models here.
from journal.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = ['author']

    def save_model(self, request, obj, form, change):
        obj.author = request.user.username
        super().save_model(request, obj, form, change)
