from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants.users import NAME_LENGTH, EMAIL_LENGTH, ROLE_LENGTH


class UserManager(BaseUserManager):
    """
    Менеджер пользователей.

    Этот менеджер обеспечивает создание и управление пользователями в системе.

    Methods:
        - _create_user(email, password, **extra_fields): Создает и сохраняет
        пользователя с заданным email и паролем.
        - create_user(email, password=None, **extra_fields): Создает и
        сохраняет обычного пользователя.
        - create_superuser(email, password, **extra_fields): Создает и
        сохраняет суперпользователя.

    Attributes:
        - use_in_migrations: Флаг, указывающий, что этот менеджер
        используется в миграциях.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с заданным email и паролем.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля пользователя.
        :return: Созданный пользователь.
        """
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля пользователя.
        :return: Созданный пользователь.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и сохраняет суперпользователя.

        :param email: Email суперпользователя.
        :param password: Пароль суперпользователя.
        :param extra_fields: Дополнительные поля суперпользователя.
        :return: Созданный суперпользователь.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """

    """
    USER = 'user'
    ADMIN = 'admin'

    ROLES = (
        (USER, USER),
        (ADMIN, ADMIN)
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    first_name = models.CharField(
        'Имя',
        max_length=NAME_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=NAME_LENGTH
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_LENGTH,
        unique=True,
    )
    telegram_id = models.IntegerField(
        'Telegram id',
        null=True,
        blank=True,
        help_text='Введите ваш Telegram id'
    )
    role = models.CharField(
        'Роль',
        max_length=ROLE_LENGTH,
        choices=ROLES,
        default=USER,
        blank=True
    )
    username: None = None

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        :return: Строковое представление в формате "Имя Фамилия".
        """
        return f'{self.first_name} {self.last_name}'
