import json
from datetime import datetime
from rest_framework.mixins import UpdateModelMixin
from django.db.models import Subquery, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from drf_yasg.utils import swagger_auto_schema
from api.v1.serializers import (DealerSerializer,
                                DealerParsingSerializer,
                                ProductSerializer,
                                MatchSerializer,
                                DealerParsingPostponeSerializer,
                                DealerParsingNoMatchesSerializer,
                                MatchingPredictionsSerializer)
from backend.celery import make_predictions
from core.pagination import CustomPagination
from products.models import (Dealer, DealerParsing, Product, Match,
                             MatchingPredictions)
from .filters import (DealerParsingFilter,
                      DealerParsingIsMatchedFilter,
                      DealerParsingIsPostponedFilter,
                      DealerParsingHasNoMatchesFilter)


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # TODO: Добавить проверку авторизован ли пользователь

        return Response({'detail': 'Вы вышли из системы.'},
                        status=HTTP_204_NO_CONTENT)


class DealerViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет дилеров"""
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    pagination_class = CustomPagination


class DealerParsingViewSet(viewsets.ModelViewSet):
    """Вьюсет DealerParsing"""
    queryset = DealerParsing.objects.all()
    serializer_class = DealerParsingSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = DealerParsingFilter


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет предоставляющий список продуктов Prosept."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination


class PostponeViewSet(viewsets.ReadOnlyModelViewSet, UpdateModelMixin):
    """
    ViewSet для работы с отложенными элементами DealerParsing.

    Позволяет просматривать отложенные элементы и выполнять
    частичное обновление.

    Атрибуты класса:
        - `queryset`: набор данных для запросов;
        - `serializer_class`: класс сериализатора для преобразования данных;
        - `pagination_class`: класс пагинации для разбивки
        результатов на страницы.

    Методы:
        - `list`: возвращает список отложенных элементов
        с применением пагинации;
        - `retrieve`: возвращает детали отдельного отложенного элемента;
        - `partial_update`: частично обновляет отложенный элемент;
        - `update`: возвращает ошибку метода не разрешен (HTTP 405).

    Атрибуты запроса:
        - `request`: объект запроса;
        - `args`: дополнительные аргументы;
        - `kwargs`: дополнительные именованные аргументы.

    Возвращает:
        - `Response`: объект ответа с данными отложенных элементов
    или ошибкой метода не разрешен.
    """
    queryset = DealerParsing.objects.all()
    serializer_class = DealerParsingPostponeSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        Возвращает список отложенных элементов с применением пагинации.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
        - `Response`: объект ответа с данными отложенных
        элементов и метаданными пагинации.

        Пример использования:
            GET /api/postpone/
        """
        queryset = DealerParsing.objects.filter(is_postponed=True)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает детали отдельного отложенного элемента.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
            - `Response`: объект ответа с данными отдельного
            отложенного элемента.

        Пример использования:
            GET /postpone/<id>/
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет отложенный элемент.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
            - `Response`: объект ответа с обновленными данными отложенного элемента.

        Пример использования:
            PATCH /postpone/<id>/
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        """
        Возвращает ошибку метода не разрешен (HTTP 405).

        Этот метод будет скрыт в Swagger.

        Возвращает:
        - `Response`: объект ответа с ошибкой метода не разрешен.
        """
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


class NoMatchesViewSet(viewsets.ReadOnlyModelViewSet, UpdateModelMixin):
    """
    ViewSet для работы с элементами DealerParsing, у которых
    нет соответствий.

    Позволяет просматривать элементы без соответствий и
    выполнять частичное обновление.

    Атрибуты класса:
    - `queryset`: набор данных для запросов;
    - `serializer_class`: класс сериализатора для преобразования данных;
    - `pagination_class`: класс пагинации для разбивки
    результатов на страницы.

    Методы:
    - `list`: возвращает список элементов без соответствий
    с применением пагинации;
    - `retrieve`: возвращает детали отдельного элемента без соответствий;
    - `partial_update`: частично обновляет элемент без соответствий;
    - `update`: возвращает ошибку метода не разрешен (HTTP 405).

    Атрибуты запроса:
    - `request`: объект запроса;
    - `args`: дополнительные аргументы;
    - `kwargs`: дополнительные именованные аргументы.

    Возвращает:
    - `Response`: объект ответа с данными элементов без
    соответствий или ошибкой запрещённого метода PUT.
    """
    queryset = DealerParsing.objects.all()
    serializer_class = DealerParsingNoMatchesSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        Возвращает список элементов без соответствий с применением пагинации.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
            - `Response`: объект ответа с данными элементов без
            соответствий и метаданными пагинации.

        Пример использования:
            GET /no-matches/
        """
        queryset = DealerParsing.objects.filter(has_no_matches=True)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает детали отдельного элемента без соответствий.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
            - `Response`: объект ответа с данными отдельного
            элемента без соответствий.

        Пример использования:
            GET /no-matches/<id>/
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет элемент без соответствий.

        Аргументы:
            - `request`: объект запроса;
            - `args`: дополнительные аргументы;
            - `kwargs`: дополнительные именованные аргументы.

        Возвращает:
            - `Response`: объект ответа с обновленными данными
            элемента без соответствий.

        Пример использования:
            PATCH /no-matches/<id>/
        """
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def update(self, request, *args, **kwargs):
        """
        Возвращает ошибку метода не разрешен (HTTP 405).

        Этот метод будет скрыт в Swagger.

        Возвращает:
        - `Response`: объект ответа с ошибкой метода не разрешен.
        """
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)


class MatchViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с мэтчами.

    Позволяет создавать, частично обновлять и удалять мэтчи.

    Attributes:
        queryset (QuerySet): Запрос для получения всех объектов Match.
        serializer_class (Type[MatchSerializer]): Класс сериализатора Match.
        pagination_class (None): Класс пагинации (не используется).

    Methods:
        create(self, request, *args, **kwargs): Создает новый мэтч, связывая
            объекты DealerParsing, Dealer и Product. Проверяет уникальность
            создаваемого мэтча.
        partial_update(self, request, *args, **kwargs): Частично обновляет
            данные мэтча, включая изменение даты в поле matching_date.
        destroy(self, request, *args, **kwargs): Удаляет мэтч, устанавливая
            is_matched в False и убирая дату из поля matching_date.

    Raises:
        HTTP_404_NOT_FOUND: Если объект мэтча не найден.
    """
    queryset = Match.objects.all().order_by('key')
    serializer_class = MatchSerializer
    pagination_class = CustomPagination

    # TODO: Описать GET запрос, в котором будут выводиться дополнительные поля.

    def create(self, request, *args, **kwargs):
        """
        Создает новый мэтч, связывая объекты DealerParsing, Dealer и Product.
        Проверяет уникальность создаваемого мэтча.

        Args:
            request (Request): Объект запроса.
            *args: Позиционные аргументы.
            **kwargs: Ключевые аргументы.

        Returns:
            Response: Ответ с результатом создания мэтча.

        Raises:
            HTTP_400_BAD_REQUEST: Если мэтч с такими параметрами
            уже существует.
            HTTP_201_CREATED: Если мэтч успешно создан.
        """
        key = request.data.get("key")
        dealer_id = request.data.get("dealer_id")
        product_id = request.data.get("product_id")

        # Получаем объект DealerParsing по артикулу продукта.
        dealer_parsing_instance = get_object_or_404(DealerParsing,
                                                    product_key=key)
        dealer_id_instance = get_object_or_404(Dealer, id=dealer_id)
        product_id_instance = get_object_or_404(Product, id=product_id)

        # Проверяем, не существует ли уже такого мэтча.
        existing_match = Match.objects.filter(key=dealer_parsing_instance,
                                              dealer_id=dealer_id_instance,
                                              product_id=product_id_instance).first()

        if existing_match:
            return Response({'detail': 'Соответствие уже существует.'},
                            status=HTTP_400_BAD_REQUEST)

        # Создаем новый мэтч
        Match.objects.create(
            key=dealer_parsing_instance,
            dealer_id=dealer_id_instance,
            product_id=product_id_instance
        )

        dealer_parsing_instance = DealerParsing.objects.get(product_key=key)
        dealer_parsing_instance.is_matched = True
        dealer_parsing_instance.matching_date = datetime.now().strftime(
            "%Y-%m-%d")
        dealer_parsing_instance.save()

        return Response({'detail': 'Связь успешно установлена.'},
                        status=HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет данные мэтча, включая изменение
        даты в поле matching_date.

        Args:
            request (Request): Объект запроса.
            *args: Позиционные аргументы.
            **kwargs: Ключевые аргументы.

        Returns:
            Response: Ответ с результатом частичного обновления мэтча.
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


def destroy(self, request, *args, **kwargs):
    """
    Удаляет мэтч, устанавливая is_matched в False и убирая дату
    из поля matching_date.

    Args:
        request (Request): Объект запроса.
        *args: Позиционные аргументы.
        **kwargs: Ключевые аргументы.

    Returns:
        Response: Ответ с результатом удаления мэтча.

    Raises:
        HTTP_404_NOT_FOUND: Если объект мэтча не найден.
        HTTP_204_NO_CONTENT: Если мэтч успешно удалён.
    """
    try:
        instance = self.get_object()
    except Exception as error:
        return Response(
            {"detail": "Нет совпадений соответствующих данному запросу"},
            status=HTTP_404_NOT_FOUND
        )

    # Установка is_matched в False и удаление даты.
    instance.key.is_matched = False
    instance.key.matching_date = None
    instance.key.save()

    # Удаление самого мэтча.
    instance.delete()

    return Response({"detail": f"{instance}"}, status=HTTP_204_NO_CONTENT)


class MatchingPredictionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для работы с предсказаниями соответствия продуктов.

    Позволяет просматривать только актуальные предсказания, которые не имеют
        установленной связи (is_matched=False).

    Attributes:
        queryset (QuerySet): Запрос для получения всех
            объектов MatchingPredictions.
        serializer_class (Type[MatchingPredictionsSerializer]): Класс
            сериализатора MatchingPredictions.
        pagination_class (CustomPagination): Класс пагинации.
    """
    queryset = MatchingPredictions.objects.all()
    serializer_class = MatchingPredictionsSerializer
    pagination_class = CustomPagination

    # Нужно сделать выдачу только актуальных данных. Только для тех товаров
    # Дилера, которые помечены как is_matched=False.
    # Только чтение данных.

    # Показать товары, по dealer_id, фильтруя по is_matched=False.
    # Дополнительно вывести в ответе поля dealer_name, dealer_article,
    # dealer_url, prosept_name_1c, prosept_article,

    # TODO: Подумать нужна ли здесь пагинация. Пока не очень понятно.

    def list(self, request, *args, **kwargs):
        """
        Получает список актуальных предсказаний, отфильтрованных
            по позициям, у которых ещё не задана связь. Выводит в ответе API
            дополнительные поля для лучшего восприятия.

        Args:
            request (Request): Объект запроса.
            *args: Позиционные аргументы.
            **kwargs: Ключевые аргументы.

        Returns:
            Response: Ответ с данными актуальных предсказаний.
        """
        queryset = MatchingPredictions.objects.filter(
            dealer_product_id__in=DealerParsing.objects.filter(
                is_matched=False, has_no_matches=False).values('id'))
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class AnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = None
    serializer_class = DealerParsingSerializer

    def analyze(self, request, *args, **kwargs):
        existing_predictions_subquery = MatchingPredictions.objects.filter(
            dealer_product_id=OuterRef('pk')
        ).values('dealer_product_id')

        # Получаем все записи DealerParsing с is_matched=False и которых
        # нет в MatchingPredictions
        # TODO: ЭТО ПОЙДЁТ НА АНАЛИЗ. QUERYSET
        #  ТОВАРОВ ДИЛЕРОВ КОТОРЫХ НЕТ В ПРЕДИКШНАХ.
        dealer_parsing_entries = DealerParsing.objects.filter(
            is_matched=False
        ).exclude(
            pk__in=Subquery(existing_predictions_subquery)
        )
        serializer = self.get_serializer(dealer_parsing_entries, many=True)

        from django.core.serializers import serialize

        # Достаём данные о продуктах Просепт и дилерах.
        # Так же по просьбе DS достаём данные о соответствиях.

        prosept_products_queryset = Product.objects.all()
        dealer_queryset = Dealer.objects.all()
        match_queryset = Match.objects.all()

        serialized_prosept_products = serialize('json',
                                                prosept_products_queryset)
        serialized_dealers = serialize('json', dealer_queryset)
        serialized_matches = serialize('json', match_queryset)

        json_dealer_data = json.dumps(serializer.data)
        json_prosept_products = json.loads(serialized_prosept_products)
        json_dealers = json.loads(serialized_dealers)
        json_matches = json.loads(serialized_matches)

        # Проверим заведён ли у пользователя Telegram ID.
        # Это нужно для отправки ему сообщения о готовности подбора или
        # информации об ошибках.
        error_message = ''
        try:
            # Получаем текущего пользователя
            current_user = request.user
            # Проверяем, есть ли у пользователя telegram_id
            chat_id = current_user.telegram_id

        except Exception as error:
            error_message = ('Telegram ID не задан. Сообщение в '
                             'Telegram не будет отправлено.')
            chat_id = None

        # Запускаем задачу в фоновом режиме.
        # Здесь передаём данные в celery, а после в ML модель.
        make_predictions.delay(make_predictions,
                               json_dealer_data,
                               json_prosept_products,
                               json_dealers,
                               json_matches,
                               chat_id)

        return Response(
            {'detail': f'Данные успешно переданы '
                       f'в ML модель. ' + error_message},
            status=HTTP_200_OK
        )


class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    """Сбор статистики парсинга дилеров"""
    queryset = DealerParsing.objects.all()
    serializer_class = DealerParsingSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = DealerParsingIsMatchedFilter
    # Пока ничего не получилось.
    