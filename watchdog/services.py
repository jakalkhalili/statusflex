from threading import Timer

import requests
from django.utils import timezone

from journal.services import create_system_failure_report, create_system_recovery_report


def count_unavailable_services(services):
    i = 0
    for service in services:
        if service.available is False:
            i += 1
    return i

def watchdog_create_system_failure_report(service):
    create_system_failure_report(service)

def watchdog_create_system_recovery_report(service):
    create_system_recovery_report(service)


def update_all_service_statistics(services):
    for service in services:
        service.update_service_statistics()