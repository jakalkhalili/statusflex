from django.contrib import admin
from django.urls import path

from journal import views

urlpatterns = [
    path('reports/<int:service_id>/', views.service_reports, name='service_reports')
]
