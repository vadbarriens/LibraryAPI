from rest_framework import serializers

from library.models import Author, Book, Loan
from library.validators import validate_profanity


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора"""

    class Meta:
        """Метаданные"""
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """Сериализатор для книги"""
    title = serializers.CharField(validators=[validate_profanity])
    description = serializers.CharField(validators=[validate_profanity])

    class Meta:
        """Метаданные"""
        model = Book
        fields = "__all__"


class LoanSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи книг"""

    class Meta:
        """Метаданные"""
        model = Loan
        fields = "__all__"
