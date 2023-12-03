from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema

from core.pagination import CustomPagination
from users.models import User
from users.schemas import USER_SCHEMA
from users.serializers import CustomUserSerializer


@extend_schema_view(**USER_SCHEMA,
                    activation=extend_schema(exclude=True),
                    resend_activation=extend_schema(exclude=True),
                    reset_password=extend_schema(exclude=True),
                    reset_password_confirm=extend_schema(exclude=True),
                    set_password=extend_schema(exclude=True),)
class CustomUserViewSet(UserViewSet):
    """
    Вьюсет для работы с пользователями.

    Позволяет просматривать, создавать, обновлять и удалять пользователей.

    Attributes:
        serializer_class (Type[CustomUserSerializer]): Класс сериализатора
            пользователей.
        pagination_class (Type[CustomPagination]): Класс пагинации.

    Methods:
        get_queryset(self): Возвращает queryset в зависимости от типа запроса.
        activation(self, *args, **kwargs): Метод для активации пользователя
            (скрыт в Swagger).
        resend_activation(self, *args, **kwargs): Метод для повторной
            отправки активации (скрыт в Swagger).
        set_password(self, *args, **kwargs): Метод для установки пароля
            (скрыт в Swagger).
        reset_password(self, *args, **kwargs): Метод для сброса пароля
            (скрыт в Swagger).
        reset_password_confirm(self, *args, **kwargs): Метод для подтверждения
            сброса пароля (скрыт в Swagger).
    """

    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Возвращает queryset в зависимости от типа запроса.
        """
        if self.action == 'retrieve':
            # Если это запрос на получение одного пользователя
            return User.objects.filter(pk=self.kwargs['id'])
        else:
            # В противном случае возвращаем всех пользователей
            return User.objects.all()
