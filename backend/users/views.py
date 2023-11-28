from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema

# from api.v1.permissions import IsAdminUser
# from core.celery.celery_app import send_activation_email, activate_user
# from core.pagination import CustomPagination
from users.models import User
from users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """

    """

    serializer_class = CustomUserSerializer

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

    @swagger_auto_schema(auto_schema=None)
    def activation(self, *args, **kwargs):
        """
        Этот метод будет скрыт в Swagger.
        """
        return super().activation(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def resend_activation(self, *args, **kwargs):
        """
        Этот метод будет скрыт в Swagger.
        """
        return super().resend_activation(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def set_password(self, *args, **kwargs):
        """
        Этот метод будет скрыт в Swagger.
        """
        return super().set_password(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def reset_password(self, *args, **kwargs):
        """
        Этот метод будет скрыт в Swagger.
        """
        return super().reset_password(*args, **kwargs)

    @swagger_auto_schema(auto_schema=None)
    def reset_password_confirm(self, *args, **kwargs):
        """
        Этот метод будет скрыт в Swagger.
        """
        return super().reset_password_confirm(*args, **kwargs)
