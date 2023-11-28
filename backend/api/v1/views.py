from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from backend.celery import long_running_task


from products.models import Dealer, Price, Product, Match
from .serializers import (DealerSerializer,
                          PriceSerializer,
                          ProductSerializer,
                          MatchSerializer)



class AuthViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def logout(self, request):
        response = JsonResponse({'detail': 'Вы разлогинились.'})

        # TODO: Добавить проверку авторизован ли пользователь

        return response


class TelegramTest(viewsets.ViewSet):
    def send(self, request):
        # Получаем текущего пользователя
        current_user = request.user

        # Проверяем, есть ли у пользователя telegram_id
        chat_id = current_user.telegram_id

        # Запускаем задачу в фоновом режиме
        long_running_task.delay(chat_id)

        return Response({"detail": "Задача поставлена в очередь для выполнения."}, status=HTTP_200_OK)


class DealerViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет дилеров"""
    permission_classes = (IsAuthenticatedOrReadOnly)
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    pagination_class = None


class PriceViewSet(viewsets.ModelViewSet):
    """Вьюсет цен дилеров"""
    permission_classes = (IsAuthenticatedOrReadOnly)
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет продукта заказчика"""
    permission_classes = (IsAuthenticatedOrReadOnly)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None


class MatchViewSet(viewsets.ModelViewSet):
    """Вьюсет мэтча"""
    permission_classes = (IsAuthenticatedOrReadOnly)
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    pagination_class = None



