from book.views import TestAPI, LoginApi, LogoutApi
from django.urls import path

urlpatterns = [
    # path("books/", BookListApiView.as_view(), name="book-list"),
    path("login/", LoginApi.as_view()),
    path("logout/", LogoutApi.as_view()),
    path("get/", TestAPI.as_view()),
    
    # path("books/<int:book_id>", BookDetailApiView.as_view(), name="book-detail"),
]