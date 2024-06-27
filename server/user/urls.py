from .views import LoginApi, deviceApi
from django.urls import path

urlpatterns = [
    path("login/", LoginApi.as_view()),
    path("device/", deviceApi.as_view()),
]