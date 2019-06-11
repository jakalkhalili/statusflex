from django.shortcuts import render

from .models import Service
# Create your views here.

from .services import count_unavailable_services, update_all_service_statistics


def services_list(request):
    services = Service.objects.all()
    unavailable_services = count_unavailable_services(services)

    update_all_service_statistics(services)

    if unavailable_services == 0:
        services_status = 0
    elif unavailable_services == Service.objects.count():
        services_status = 1
    else:
        services_status = 2

    return render(request, 'watchdog/services_list.html', {"services": services,
                                                     "services_status": services_status,
                                                     "unavailable_services": unavailable_services,
                                                     "all_services": services.count()})
