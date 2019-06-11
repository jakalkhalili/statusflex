from django.conf import settings
from django.db import models

# Create your models here.



class ReportType(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Report(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    service = models.ForeignKey('watchdog.Service', null=True, blank=True, on_delete=models.SET_NULL)
    author = models.TextField(max_length=50)

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(ReportType, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
