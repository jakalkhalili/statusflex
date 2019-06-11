from django.shortcuts import render

# Create your views here.
from watchdog.models import Service
from journal.models import Report

def service_reports(request, service_id):
    reports = Report.objects.filter(service=service_id).order_by("-added")
    service = Service.objects.get(id=service_id)
    service.update_service_statistics()
    return render(request, "journal/reports_list.html", {"reports": reports, "service": service})