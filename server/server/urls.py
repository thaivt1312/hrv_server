from .views import LogoutApi, LoginApi, checkDevice, HRVDataAPI, SoundDataAPI
# from .account_view import accountRegisterApi, adminAccountRegisterApi, LoginApi, checkTokenApi
from django.urls import path

urlpatterns = [
    # path("logout/", LogoutApi.as_view()),
    # path("login/", LoginApi.as_view()),
    # path("register/newDevice", LoginApi.as_view()),
    path("checkDevice/", checkDevice.as_view()),
    path("post/hrData/", HRVDataAPI.as_view()),
    path("post/record/", SoundDataAPI.as_view()),
    
]