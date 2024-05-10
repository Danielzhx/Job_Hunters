from django.urls import path
from . import views

app_name = 'profiles'
urlpatterns = [
    path("", views.index, name="profiles"),
    path("applications", views.view_applications, name="applications")
    # Apply for job
    ]   