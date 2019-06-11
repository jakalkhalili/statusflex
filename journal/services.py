from .models import Report, ReportType

def create_system_report(title, content, service, report_type):
    report = Report()
    report.title = "Statusflex: %s" % title
    report.author = "Statusflex"
    report.service = service
    report.content = content
    report.type = report_type
    report.save()


def create_system_failure_report(service):
    create_system_report("Service failure",
                         "Statusflex detected that service not responding.",
                         service,
                         ReportType.objects.get(title="Failure"))


def create_system_recovery_report(service):
    create_system_report("Service recovered",
                         "Statusflex detected that service now responding.",
                         service,
                         ReportType.objects.get(title="Success"))
