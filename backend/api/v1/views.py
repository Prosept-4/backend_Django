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

        # Можно преобразовать в json и отдавать его.
        # Если пойдёт OrderedDict, то отдаём просто serializer.data.
        json_data_to_ml = json.dumps(serializer.data)

        try:
            # Получаем текущего пользователя
            current_user = request.user
            # Проверяем, есть ли у пользователя telegram_id
            chat_id = current_user.telegram_id

        except Exception as error:
            error_message = ('Telegram ID не задан. Сообщение в '
                             'Telegram не будет отправлено.')
            chat_id = None

        # Запускаем задачу в фоновом режиме
        make_predictions.delay(json_data_to_ml, chat_id)

        # Здесь передаём данные в celery, а после в ML модель.
        # start_ml_celery.delay(json_data_to_ml)

        return Response(
            {'detail': 'Данные успешно переданы в ML модель.'},
            status=HTTP_200_OK
        )
