from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from backend.celery import long_running_task



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
