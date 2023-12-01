from drf_spectacular.utils import extend_schema, OpenApiParameter

# AnalysisViewSet
ANALYSIS_SCHEMA = {
    'analyze': extend_schema(
        description='Запускает анализ данных и отправляет уведомление.',
        summary='Запустить анализ данных и отправить уведомление.',
    ),

}

# AuthViewSet
LOGOUT_SCHEMA = {
    'logout': extend_schema(
        description='Выход пользователя из системы.',
        summary='Выход пользователя из системы.',
    )
}

# DealerViewSet
DEALER_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список дилеров с использованием пагинации.',
        summary='Получить список дилеров.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детали отдельного дилера.',
        summary='Получить детали дилера.',
    )
}

# DealerParsingViewSet
DEALER_PARSING_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список отложенных элементов DealerParsing с применением пагинации.',
        summary='Получить список отложенных элементов DealerParsing.'
    ),
    'retrieve': extend_schema(
        description='Возвращает детали отдельного отложенного элемента DealerParsing.',
        summary='Получить детали отложенного элемента DealerParsing.',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет отложенный элемент DealerParsing.',
        summary='Частично обновить отложенный элемент DealerParsing.',
        parameters=[
            OpenApiParameter(
                name='is_postponed',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отложенности.',
                required=True,
                type=bool,
            ),
        ],
    )
}

# ProductViewSet
PRODUCT_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список продуктов Prosept с использованием пагинации.',
        summary='Получить список продуктов Prosept.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детали отдельного продукта Prosept.',
        summary='Получить детали продукта Prosept.',
    )
}

# PostponeViewSet
POSTPONE_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список отложенных элементов DealerParsing с применением пагинации.',
        summary='Получить список отложенных элементов DealerParsing.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детали отдельного отложенного элемента DealerParsing.',
        summary='Получить детали отложенного элемента DealerParsing.',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет отложенный элемент DealerParsing.',
        summary='Частично обновить отложенный элемент DealerParsing.',
        parameters=[
            OpenApiParameter(
                name='is_postponed',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отложенности.',
                required=True,
                type=bool,
            ),
        ],
    ),
}

# NoMatchesViewSet
NO_MATCHES_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список элементов без соответствий с применением пагинации.',
        summary='Получить список элементов без соответствий.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детали отдельного элемента без соответствий.',
        summary='Получить детали элемента без соответствий.',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет элемент без соответствий.',
        summary='Частично обновить элемент без соответствий.',
        parameters=[
            OpenApiParameter(
                name='has_no_matches',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отсутствия соответствий.',
                required=True,
                type=bool,
            ),
        ],
    ),
}

# MatchViewSet
MATCH_SCHEMA = {
    'create': extend_schema(
        description='Создает новый мэтч, связывая объекты DealerParsing, Dealer и Product.',
        summary='Создать новый мэтч.',
        parameters=[
            OpenApiParameter(
                name='key',
                location=OpenApiParameter.QUERY,
                description='Артикул продукта.',
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name='dealer_id',
                location=OpenApiParameter.QUERY,
                description='ID дилера.',
                required=True,
                type=int,
            ),
            OpenApiParameter(
                name='product_id',
                location=OpenApiParameter.QUERY,
                description='ID продукта.',
                required=True,
                type=int,
            ),
        ],
    ),
    'partial_update': extend_schema(
        description='Частично обновляет данные мэтча, включая изменение даты в поле matching_date.',
        summary='Частично обновить мэтч.',
        parameters=[
            OpenApiParameter(
                name='matching_date',
                location=OpenApiParameter.QUERY,
                description='Новая дата соответствия.',
                required=False,
                type=str,
            ),
        ],
    ),
    'destroy': extend_schema(
        description='Удаляет мэтч, устанавливая is_matched в False и убирая дату из поля matching_date.',
        summary='Удалить мэтч.',
    ),

}

# MatchingPredictionsViewSet
MATCHING_PREDICTIONS_SCHEMA = {
    'list': extend_schema(
        description='Получает список актуальных предсказаний, отфильтрованных по позициям, у которых ещё не задана связь.',
        summary='Получить список актуальных предсказаний.',
        parameters=[
            OpenApiParameter(
                name='dealer_id',
                location=OpenApiParameter.QUERY,
                description='Идентификатор дилера.',
                required=False,
                type=int,
            ),
            OpenApiParameter(
                name='is_matched',
                location=OpenApiParameter.QUERY,
                description='Указывает, имеет ли связь позиция.',
                required=False,
                type=bool,
            ),
        ],
    ),
}
