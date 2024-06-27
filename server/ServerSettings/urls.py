# from django.contrib import admin
from django.urls import path, include

from administrator import urls as administratorUrls

from user import urls as userUrls

from server import urls as serverUrls

urlpatterns = [
    path('admin/', include(administratorUrls)),
    path('user/', include(userUrls)),
    path('api/', include(serverUrls)),
]
