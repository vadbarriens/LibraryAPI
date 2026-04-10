from django.contrib import admin

from library.models import Author, Book, Loan


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'fullname')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'title', 'author')


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """Класс для отображения модели в админке"""
    list_display = ('id', 'book', 'borrower')
