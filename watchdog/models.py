import math

from django.db import models
import requests

# Create your models here.
from django.utils import timezone

from watchdog.services import watchdog_create_system_failure_report, watchdog_create_system_recovery_report


class Service(models.Model):
    name = models.CharField(max_length=100)
    check_url = models.CharField(max_length=255)

    last_failed = models.DateTimeField(auto_now=False, null=True)
    recovered = models.DateTimeField(auto_now=False, null=True)
    failure = models.BooleanField(default=False)
    prechecked = models.BooleanField(default=False)
    precheck_time = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

    enable_prechecking = models.BooleanField(default=True)
    enable_automatic_reports = models.BooleanField(default=True)

    downtime = models.IntegerField(default=0)
    last_downtime_updated = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    added = models.DateTimeField(auto_now_add=True, auto_now=False)

    @property
    def available(self):
        try:
            r = requests.get(self.check_url, timeout=10)
            if self.enable_prechecking:
                self.prechecked = False
            return True
        except:
            self.update_downtime()
            if self.enable_prechecking:
                if self.prechecked is False:
                    self.prechecked = True
                    self.precheck_time = timezone.now()
                    return True
                elif self.precheck_time_difference_passed:
                    return False
                else:
                    return True
            else:
                return False
        finally:
            if self.enable_prechecking:
                self.save()

    @property
    def calculate_working_time(self):
        if not self.available:
            return "Not working"
        if self.recovered:
            time_diff = timezone.now() - self.recovered
            return str(time_diff).split(".")[0]
        else:
            return "Never recovered"

    def calculate_precheck_time_diferrence(self):
        return timezone.now().timestamp() - self.precheck_time.timestamp()

    @property
    def precheck_time_difference_passed(self):
        if self.prechecked:
            if self.calculate_precheck_time_diferrence() >= 60:
                return True
        return False

    @property
    def waiting_for_response(self):
        if self.prechecked:
            if 30 <= self.calculate_precheck_time_diferrence() < 60:
                return True
        return False

    def update_downtime(self):
        delta = timezone.now().timestamp() - self.last_downtime_updated.timestamp()
        self.downtime = self.downtime + delta
        self.last_downtime_updated = timezone.now()
        self.save()

    def update_service_statistics(self):
        if self.enable_automatic_reports:
            if self.available is False and self.failure is False:
                self.last_failed = timezone.now()
                self.failure = True
                self.save()
                watchdog_create_system_failure_report(self)
            elif self.available is True and self.failure is True:
                self.recovered = timezone.now()
                self.failure = False
                self.save()
                watchdog_create_system_recovery_report(self)

    @property
    def calculate_uptime(self):
        if self.last_downtime_updated:
            return math.floor((100 - ((self.downtime / self.added.timestamp()) * 100)) * 20) / 20
        else:
            return "NaN"

    @property
    def get_last_failed(self):
        if self.last_failed:
            return self.last_failed
        return "Never"

    def __str__(self):
        return self.name

