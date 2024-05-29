from django.contrib import admin
from django.urls import path, include
from server import urls as serverUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(serverUrls)),
]
