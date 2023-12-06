import asyncio
import logging

from django.core.mail import send_mail
from telegram import Bot
from telegram.error import BadRequest, InvalidToken, NetworkError, TimedOut

from backend.celery import app
from backend.settings import DEFAULT_FROM_EMAIL
from core.environment import BOT_TOKEN
from products.models import MatchingPredictions
from script import main_function

bot = Bot(token=BOT_TOKEN)
logger = logging.getLogger(__name__)


@app.task
async def send_telegram_message(chat_id, email, message):

    def _telegram_error(error_message, error_detail):
        return ('Сообщение в Telegram не отправлено! '
                f'{error_message}!'
                ' Отправляем письмо на почту...'
                f' Детали ошибки: {error_detail}')

    try:
        async with bot:
            await bot.send_message(chat_id=chat_id, text=message)
        logger.info('Сообщение в Telegram успешно отправлено!')

        return

    except BadRequest as err:
        msg = 'chat_id пользователя не задан! '
        error = err

    except InvalidToken as err:
        msg = 'Недействительный токен! '
        error = err

    except TimedOut as err:
        msg = 'Истекло время запроса! '
        error = err

    except NetworkError as err:
        msg = 'Проверьте возможность подключения к серверам Telegram! '
        error = err

    except Exception as err:
        msg = 'Произошла непредвиденная ошибка! '
        error = err

    # Логируем ошибку.
    logger.error(_telegram_error(msg, error))

    try:
        subject = 'Анализ данных Prosept'
        message = (f'Привет, дорогой друг. Это письмо пришло тебе '
                   f'потому что ты запустил процесс анализа данных в сервисе '
                   f'соответствий.\n\nСпешим сообщить тебе, что анализ прошёл '
                   f'успешно. При следующем запросе тебе будут предоставлены '
                   f'обновлённые данные.\n\nПриятного тебе трудового дня! '
                   f'P.S. Не забывай прерываться на чай :)\n\nС любовью, '
                   f'Команда 4 <3')
        send_from = DEFAULT_FROM_EMAIL
        send_to = [email]

        send_mail(subject, message, send_from, send_to, fail_silently=False)

    except Exception as error:
        logger.error(f'Непредвиденная ошибка отправки письма: {error}')


@app.task(rate_limit='1/m')
def make_predictions(json_parser, json_products, email, chat_id=None):
    # TODO: Сюда ставим вызов ML модели, передаём в неё массив для анализа.
    message = f'Query -   {json_parser}.\n\n query2  - {json_products}'
    asyncio.run(send_telegram_message(chat_id, email, message))
    ml_results = main_function(json_parser, json_products)

    # logger.error(ml_results)
    for result in ml_results:
        for dealer_product_id, *prosept_product_ids in result.items():
            for procept_id in prosept_product_ids:
                MatchingPredictions.objects.create(
                    dealer_product_id=int(dealer_product_id),
                    prosept_product_id=str(procept_id)
                )

    # for zapis in ml_results:
    #     dealer_product_id, *prosept_product_ids = zapis
    #     for znachenie in prosept_product_ids:
    #             MatchingPredictions.objects.create(
    #                 dealer_product_id=int(dealer_product_id),
    #                 prosept_product_id=str(znachenie)
    #             )

    # Обработка результатов ML и создание записей в БД
    # for zapis in ml_results:
    #     for dealer_product_id, prosept_product_ids in zapis.items():
    #         for prosept_product_id in prosept_product_ids:
    #             MatchingPredictions.objects.create(
    #                 dealer_product_id=dealer_product_id,
    #                 prosept_product_id=prosept_product_id
    #             )

    message = f'Расчёт соответствий завершён успешно.'
    logger.info(message)

    asyncio.run(send_telegram_message(chat_id, email, message))
