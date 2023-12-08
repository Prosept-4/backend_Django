from drf_spectacular.utils import extend_schema

# CustomUserViewSet
USER_SCHEMA = {
    'list': extend_schema(
        description='Получение списка всех пользователей с '
                    'использованием пагинации.',
        summary='Получить список всех пользователей с '
                'использованием пагинации.',
    ),
    'retrieve': extend_schema(
        description='Получение детальной информации о пользователе.',
        summary='Получить детальную информацию о пользователе.',
    ),
    'create': extend_schema(
        description='Зарегистрировать нового пользователя. '
                    'Поле telegram_id является необязательным.',
        summary='Регистрация нового пользователя.',
    ),
    'update': extend_schema(
        description='Полностью изменить данные пользователя.',
        summary='Полное изменение данных пользователя.',
    ),
    'partial_update': extend_schema(
        description='Частично изменить данные пользователя.',
        summary='Частичное изменение данных пользователя.',
    ),
    'destroy': extend_schema(
        description='Удалить пользователя.',
        summary='Удаление пользователя.',
    ),
    'me': extend_schema(
        description='Получить, полностью или частично изменить данные '
                    'текущего пользователя.',
        summary='Получение, полное и частичное изменение данных '
                'текущего пользователя.',
    ),
}
