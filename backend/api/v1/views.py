import json

from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from api.v1.serializers import (DealerSerializer,
                                DealerParsingSerializer,
                                ProductSerializer,
                                MatchSerializer)
from backend.celery import make_predictions
from products.models import (Dealer, DealerParsing, Product, Match,
                             MatchingPredictions)


class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def logout(self, request):
        response = JsonResponse({'detail': 'Вы разлогинились.'})

        # TODO: Добавить проверку авторизован ли пользователь

        return response


class DealerViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет дилеров"""
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    pagination_class = None


class DealerParsingViewSet(viewsets.ModelViewSet):
    """Вьюсет DealerParsing"""
    queryset = DealerParsing.objects.all()
    serializer_class = DealerParsingSerializer
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет продукта заказчика"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None


class MatchViewSet(viewsets.ModelViewSet):
    """Вьюсет мэтча"""
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = None

    def post(self):
        # Проверяем есть ли запись мэтча в таблице.
        # Если записи нет - создаём мэтч.
        # В DealerParsing меняем is_matched на True и добавляем дату в
        # Поле matching_date.
        pass

    def patch(self):
        # При PATCH запросе проверяем есть ли запись мэтча в таблице.
        # Если запись есть — у текущей записи меняем в DealerParsing поле
        # is_matched на False и убираем дату из поля matching_date.
        # После этого меняем связь на новую. Далее по аналогии.
        # Для новой связи в DealerParsing меняем is_matched на
        # True и добавляем дату в поле matching_date.
        pass

    def delete(self):
        # При delete запросе проверяем есть ли запись мэтча в таблице.
        # Если запись есть — сначала в DealerParsing меняем is_matched на
        # False и удаляем дату из поля matching_date.
        # После этого удаляем сам мэтч из таблицы.
        pass

class MatchingPredictionsViewSet(viewsets.ModelViewSet):
    """Вьюсет мэтч предикшнов"""
    queryset = MatchingPredictions.objects.all()
    serializer_class = MatchSerializer
    pagination_class = None


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
