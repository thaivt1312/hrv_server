from .views import LogoutApi, checkDevice, HRVDataAPI, SoundDataAPI
from django.urls import path

urlpatterns = [
    path("logout/", LogoutApi.as_view()),
    path("login/checkDevice/", checkDevice.as_view()),
    path("post/hrData/", HRVDataAPI.as_view()),
    path("post/record/", SoundDataAPI.as_view()),
    
]