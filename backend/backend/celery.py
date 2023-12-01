import asyncio
import logging

from celery import Celery
from telegram import Bot

from core.environment import BOT_TOKEN
# from products.models import MatchingPredictions

logger = logging.getLogger(__name__)

app = Celery('celery', broker='redis://redis:6379/0')


@app.task
async def send_telegram_message(chat_id, message):
    bot = Bot(token=BOT_TOKEN)
    if chat_id is not None:
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            logger.info('Сообщение в Telegram успешно отправлено!')
        except Exception as err:
            logger.error(f'Сообщение не отправлено! Текст ошибки: {err}')

    # TODO: Если у пользователя не задан TELEGRAM_ID - отправить письмо
    #  на почту.
    logger.warning(f'Сообщение не отправлено! '
                   f'Не задан Telegram ID пользователя! '
                   f'Отправляем письмо на почту...')

    try:
        # TODO: Отправить письмо
        pass
    except Exception as error:
        pass
        # TODO: Дать в логи ошибку если не отправилось.


@app.task
def make_predictions(data, chat_id=None):
    try:
        # TODO: Сюда ставим вызов ML модели, передаём в неё массив для анализа.
        # ml_results = start_ml(data)

        # Обработка результатов ML и создание записей в БД
        # for dealer_product_id, prosept_product_ids in ml_results.items():
        #     for prosept_product_id in prosept_product_ids:
        #         MatchingPredictions.objects.create(
        #             dealer_product_id=dealer_product_id,
        #             prosept_product_id=prosept_product_id
        #         )

        message = 'Расчёт совпадений завершён успешно.'
        logger.info(message)

    except Exception as error:
        message = f'Расчёт завершён с ошибкой: {error}'
        logger.error(message)

    asyncio.run(send_telegram_message(chat_id, message))
