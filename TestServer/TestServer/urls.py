from django.contrib import admin
from django.urls import path, include
from book import urls as bookUrls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(bookUrls)),
]
