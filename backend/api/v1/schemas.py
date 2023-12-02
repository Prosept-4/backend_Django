from drf_spectacular.utils import extend_schema, OpenApiParameter

# AnalysisViewSet
ANALYSIS_SCHEMA = {
    'analyze': extend_schema(
        description=('Запускает анализ данных и отправляет уведомление. '
                     'Анализ данных выполняется в фоне.\n\nПосле завершения '
                     'анализа оператору приходит сообщение в Telegram, если '
                     'при регистрации он указал свой Telegram ID. Если ID не '
                     'указан - сообщение приходит на электронную почту '
                     'оператора.\n\n По итогу анализа все данные полученные '
                     'от ML модели записываются в БД в таблицу '
                     'products_matchingpredictions.'),
        summary='Запустить анализ данных и отправить уведомление.'
    ),
}

# AuthViewSet
LOGOUT_SCHEMA = {
    'logout': extend_schema(
        description='Выйти из системы.',
        summary='Выход пользователя из системы.',
    )
}

# DealerViewSet
DEALER_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список всех доступных в БД дилеров с '
                    'использованием пагинации.',
        summary='Получить список всех доступных в БД дилеров с '
                'использованием пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает информацию отдельного дилера.',
        summary='Получить информацию отдельного дилера.',
    )
}

# DealerParsingViewSet
DEALER_PARSING_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список спарсенных товаров дилеров с '
                    'применением пагинации.',
        summary='Получить список спарсенных товаров дилеров с '
                'применением пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает конкретный спарсенный товар дилера',
        summary='Получить конкретный спарсенный товар дилера',
    ),
    'create': extend_schema(
        description='Ручное добавление спарсенного товара дилера',
        summary='Добавить спарсенный товар дилера вручную.',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет спарсенный товар дилера',
        summary='Частично обновить спарсенный товар дилера',
        parameters=[
            OpenApiParameter(
                name='is_postponed',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отложенности.',
                required=True,
                type=bool,
            ),
        ],
        request=None,
    ),
    'destroy': extend_schema(
        description='Удаляет из БД конкретный спарсенный товар дилера',
        summary='Удалить из БД конкретный спарсенный товар дилера',
    ),
}

# ProductViewSet
PRODUCT_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список продуктов Prosept с '
                    'применением пагинации.',
        summary='Получить список продуктов Prosept с применением пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детальную информацию отдельного '
                    'продукта Prosept.',
        summary='Получить детальную информацию отдельного продукта Prosept.',
    )
}

# PostponeViewSet
POSTPONE_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список товаров дилеров, '
                    'отмеченных как "Отложен", с применением пагинации.',
        summary='Получить список товаров дилеров, '
                'отмеченных как "Отложен", с применением пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детальную информацию отдельного товара '
                    'дилеров, отмеченного как "Отложен".',
        summary='Получить детальную информацию отдельного товара '
                'дилеров, отмеченного как "Отложен".',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет отдельный товар '
                    'дилеров, отмеченный как "Отложен", включая изменение '
                    'даты в поле postpone_date. Дата проставляется '
                    'автоматически.',
        summary='Частично обновить отдельный товар '
                'дилеров, отмеченный как "Отложен".',
        parameters=[
            OpenApiParameter(
                name='is_postponed',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отложенности.',
                required=True,
                type=bool,
            ),
            OpenApiParameter(
                name='postpone_date',
                location=OpenApiParameter.QUERY,
                description='Новая дата пометки как "Отложенный". '
                            'Проставляется автоматически.',
                required=False,
                type=str,
            ),
        ],
    ),
}

# NoMatchesViewSet
NO_MATCHES_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список товаров дилеров, отмеченных как '
                    '"Не имеет соответствий", с применением пагинации.',
        summary='Получить список товаров дилеров, отмеченных как '
                '"Не имеет соответствий", с применением пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает элемент товара дилеров, отмеченный как '
                    '"Не имеет соответствий".',
        summary='Получить элемент товара дилеров, отмеченный как '
                '"Не имеет соответствий".',
    ),
    'partial_update': extend_schema(
        description='Частично обновляет элемент товара дилеров, отмеченный '
                    'как "Не имеет соответствий", включая изменение '
                    'даты в поле has_no_matches_toggle_date. '
                    'Дата проставляется автоматически.',
        summary='Частично обновить элемент товара дилеров, отмеченный '
                'как "Не имеет соответствий".',
        parameters=[
            OpenApiParameter(
                name='has_no_matches',
                location=OpenApiParameter.QUERY,
                description='Устанавливает флаг отсутствия соответствий.',
                required=True,
                type=bool,
            ),
            OpenApiParameter(
                name='has_no_matches_toggle_date',
                location=OpenApiParameter.QUERY,
                description='Новая дата пометки как "Не имеет соответствий". '
                            'Проставляется автоматически.',
                required=False,
                type=str,
            ),
        ],
    ),
}

# MatchViewSet
MATCH_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список соответствий товаров дилеров с '
                    'товарами Просепт с применением пагинации.',
        summary='Получить список соответствий товаров дилеров с '
                'товарами Просепт с применением пагинации.',
    ),
    'retrieve': extend_schema(
        description='Возвращает детальную информацию соответствия товара '
                    'дилера с товаром Просепт.',
        summary='Получить детальную информацию соответствия товара '
                'дилера с товаром Просепт.',
    ),
    'create': extend_schema(
        description='Создает новое соответствие в БД, связывая объекты '
                    'DealerParsing, Dealer и Product.',
        summary='Создать новое соответствие в БД, связав объекты '
                'DealerParsing, Dealer и Product.',
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
        description='Частичное обновление информации соответствия товара '
                    'дилера с товаром Просепт, включая изменение '
                    'даты в поле matching_date. '
                    'Дата проставляется автоматически.',
        summary='Частично обновить информацию соответствия товара '
                'дилера с товаром Просепт, включая изменение '
                'даты в поле matching_date. Дата проставляется автоматически.',
        parameters=[
            OpenApiParameter(
                name='matching_date',
                location=OpenApiParameter.QUERY,
                description='Новая дата соответствия. '
                            'Проставляется автоматически.',
                required=False,
                type=str,
            ),
        ],
    ),
    'destroy': extend_schema(
        description='Удалить соответствие товара дилера с товаром Просепт, '
                    'установить is_matched в False и убрать дату '
                    'из поля matching_date.',
        summary='Удаляет соответствие товара дилера с товаром Просепт.',
    ),

}

# MatchingPredictionsViewSet
MATCHING_PREDICTIONS_SCHEMA = {
    'list': extend_schema(
        description='Получает список актуальных предсказаний соответствий '
                    'с применением пагинации, отфильтрованных по позициям, '
                    'у которых ещё не задана связь.',
        summary='Получить список актуальных предсказаний соответствий.',
    ),
    'retrieve': extend_schema(
        description='Получает детали актуального предсказания соответствия',
        summary='Получить детали актуального предсказания соответствия',
    ),
}
