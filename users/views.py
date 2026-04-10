from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import AllowAny

from library.pagination import MyPagination
from users.models import User
from users.serializers import UserSerializer


class UserCreateApiView(CreateAPIView):
    """Контроллер создания пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Контроллер списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = MyPagination


class UserUpdateApiView(UpdateAPIView):
    """Контроллер обновления пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Проверка на то, что может обновлять только свой профиль"""
        return self.request.user


class UserRetrieveApiView(RetrieveAPIView):
    """Контроллер получения пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Проверка на то, что может просматривать только свой профиль"""
        return self.request.user


class UserDestroyApiView(DestroyAPIView):
    """Контроллер удаления пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """Проверка на то, что может удалять только свой профиль"""
        return self.request.user
