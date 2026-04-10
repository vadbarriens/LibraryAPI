from datetime import timedelta

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from rest_framework.response import Response

from library.models import Author, Book, Loan
from users.models import User
from library.pagination import MyPagination
from library.permissions import IsOwner, IsModer
from library.serializers import AuthorSerializer, BookSerializer, LoanSerializer


class AuthorCreateAPIView(CreateAPIView):
    """Контроллер создания автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def perform_create(self, serializer):
        """Привязка пользователя при создании"""
        serializer.save(owner=self.request.user)


class AuthorListAPIView(ListAPIView):
    """Контроллер просмотра списка авторов"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = MyPagination


class AuthorUpdateAPIView(UpdateAPIView):
    """Контроллер обновления автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner]


class AuthorRetrieveAPIView(RetrieveAPIView):
    """Контроллер получения автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner]


class AuthorDestroyAPIView(DestroyAPIView):
    """Контроллер удаления автора"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsOwner | IsModer]


class BookCreateAPIView(CreateAPIView):
    """Контроллер создания книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        """Привязка пользователя при создании"""
        serializer.save(owner=self.request.user)


class BookListAPIView(ListAPIView):
    """Контроллер просмотра списка книг"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'published_date', 'pages', 'status']


class BookUpdateAPIView(UpdateAPIView):
    """Контроллер обновления книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner]


class BookRetrieveAPIView(RetrieveAPIView):
    """Контроллер получения книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner]


class BookDestroyAPIView(DestroyAPIView):
    """Контроллер удаления книги"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwner | IsModer]


class LoanCreateApiView(CreateAPIView):
    """Контроллер создания выдачи книги"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        """Переопределение метода создания"""
        book_id = request.data.get('book')
        borrower_id = request.data.get('borrower')

        book = Book.objects.get(id=book_id)
        borrower = User.objects.get(id=borrower_id)

        if book.status != 'AVAILABLE':
            return Response(
                {'error': 'Книга не доступна для выдачи'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаем запись о выдаче
        loan = Loan.objects.create(
            book=book,
            borrower=borrower,
            loan_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=14))

        # Обновляем статус книги
        book.status = 'LOANED'
        book.current_loan = loan
        book.save()

        serializer = self.get_serializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoanUpdateApiView(UpdateAPIView):
    """Контроллер для обновления выдачи книги"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def update(self, request, *args, **kwargs):
        """Переопределение метода обновления"""
        instance = self.get_object()

        # Обновляем дату возврата
        instance.return_date = timezone.now().date()
        instance.save()

        # Обновляем статус книги
        book = instance.book
        book.status = 'AVAILABLE'
        book.current_loan = None
        book.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
