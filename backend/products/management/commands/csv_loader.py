import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import (Dealer,
                             Price,
                             Product,
                             Match)


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **kwargs):
        file_path = (
            settings.BASE_DIR / 'static_data' / 'marketing_dealer.csv')
        with open(file_path, encoding='utf8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)
            Dealer.objects.all().delete()
            dealers = []
            for row in reader:
                _, name = row
                dealers.append(Dealer(name=name))
            Dealer.objects.bulk_create(dealers)

        print('Загрузка в БД прошла успешно')
