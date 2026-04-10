from django.urls import path
from library.apps import LibraryConfig

from library.views import (
    AuthorListAPIView, AuthorCreateAPIView, AuthorUpdateAPIView, AuthorDestroyAPIView, AuthorRetrieveAPIView,
    BookListAPIView, BookDestroyAPIView, BookUpdateAPIView, BookRetrieveAPIView, BookCreateAPIView, LoanCreateApiView,
    LoanUpdateApiView
)

app_name = LibraryConfig.name

urlpatterns = [
    path("author/list/", AuthorListAPIView.as_view(), name="author_list"),
    path("author/<int:pk>/detail/", AuthorRetrieveAPIView.as_view(), name="author_retrieve"),
    path("author/create/", AuthorCreateAPIView.as_view(), name="author_create"),
    path("author/<int:pk>/update/", AuthorUpdateAPIView.as_view(), name="author_update"),
    path("author/<int:pk>/delete/", AuthorDestroyAPIView.as_view(), name="author_delete"),
    path("book/list/", BookListAPIView.as_view(), name="book_list"),
    path("book/<int:pk>/detail/", BookRetrieveAPIView.as_view(), name="book_retrieve"),
    path("book/create/", BookCreateAPIView.as_view(), name="book_create"),
    path("book/<int:pk>/update/", BookUpdateAPIView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", BookDestroyAPIView.as_view(), name="book_delete"),
    path("loan/", LoanCreateApiView.as_view(), name="loan_create"),
    path("loan/<int:pk>/update/", LoanUpdateApiView.as_view(), name="loan_update"),

]
