import asyncio
import time

from celery import Celery
from telegram import Bot

from core.environment import BOT_TOKEN

app = Celery('celery', broker='redis://redis:6379/0')


@app.task
async def send_telegram_message(chat_id, message):
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        return 'Сообщение в Telegram '
    except Exception as err:
        return f'{err} сообщение не отправлено!'


@app.task
def long_running_task(chat_id):
    try:
        # TODO: Сюда ставим вызов ML модели, передаём в неё массив для анализа.
        time.sleep(10)

        message = "Расчёт завершён"

    except Exception as error:
        message = f'Расчёт завершён с ошибкой: {error}'

    asyncio.run(send_telegram_message(chat_id, message))

    return "Расчёт завершён"
