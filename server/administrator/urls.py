from .views import LoginApi, accountApi, deviceApi
from django.urls import path

urlpatterns = [
    # path("login/", LoginApi.as_view()),
    path("account/", accountApi.as_view()),
    # path("device/", deviceApi.as_view()),
]