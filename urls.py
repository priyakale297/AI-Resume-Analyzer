from django.urls import path
from .views import home, download_report

urlpatterns = [
    path("", home, name="home"),
    path("download-report/", download_report, name="download_report"),
]