from .views import TestAPI, LoginApi, LogoutApi, checkDevice, HRVDataAPI, SoundDataAPI
from django.urls import path

urlpatterns = [
    path("login/", LoginApi.as_view()),
    path("logout/", LogoutApi.as_view()),
    path("get/", TestAPI.as_view()),
    path("login/checkDevice/", checkDevice.as_view()),
    path("post/hrData/", HRVDataAPI.as_view()),
    path("post/record/", SoundDataAPI.as_view()),
    
]