from django.db import models


class Dealer(models.Model):
    """
    Модель, представляющая дилера.

    Attributes:
        name (str): Название дилера.

    Meta:
        verbose_name (str): Отображаемое имя в админке для одного объекта.
        verbose_name_plural (str): Отображаемое имя в админке
        для нескольких объектов.
        constraints (list): Список ограничений на уровне базы данных,
        в данном случае уникальность имени дилера.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Дилер'
        verbose_name_plural = 'Дилеры'
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_dealer_name',
            )
        ]

    def __str__(self) -> str:
        return self.name


class DealerParsing(models.Model):
    """
    Модель, представляющая результат работы парсера площадок дилеров.

    Attributes:
        product_key (str): Артикул товара.
        price (str): Цена товара.
        product_url (str): Адрес страницы, откуда собраны данные.
        product_name (str): Заголовок продаваемого товара.
        date (datetime): Дата получения информации.
        dealer_id (Dealer): Связь с моделью Dealer, внешний ключ для
        связи с дилером.
        is_matched (bool): Флаг, указывающий на наличие соответствия.
        has_no_matches (bool): Флаг, указывающий на отсутствие соответствий.

    Meta:
        verbose_name (str): Отображаемое имя в админке для одного объекта.
        verbose_name_plural (str): Отображаемое имя в админке
        для нескольких объектов.
    """
    product_key = models.CharField(
        verbose_name='Артикул товара',
        max_length=256,
        unique=True,
    )
    price = models.CharField(
        verbose_name='Цена',
        max_length=256,
    )
    product_url = models.URLField(
        verbose_name='Адрес страницы, откуда собранны данные',
        max_length=2560,
    )
    product_name = models.CharField(
        verbose_name='Заголовок продаваемого товара',
        max_length=256,
    )
    date = models.DateField(
        verbose_name='Дата получения информации'
    )
    dealer_id = models.ForeignKey(
        Dealer,
        verbose_name='Дилер ID',
        related_name='parsing_entries',
        to_field='id',
        on_delete=models.CASCADE,
    )
    is_matched = models.BooleanField(
        default=False,
    )
    matching_date = models.DateField(
        verbose_name='Дата связывания',
        null=True,
        blank=True
    )
    has_no_matches = models.BooleanField(
        default=False,
    )
    has_no_matches_toggle_date = models.DateField(
        verbose_name='Дата пометки "Нет совпадений"',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Товар дилера'
        verbose_name_plural = 'Товары дилеров'

    def __str__(self) -> str:
        return self.product_name


class Product(models.Model):
    """
    Модель, представляющая список товаров, которые производит
    и распространяет Prosept.

    Attributes:
        id_product (str): ID товара.
        article (str): Артикул товара.
        ean_13 (str): Код товара.
        name (str): Название товара.
        cost (str): Стоимость товара.
        recommended_price (str): Рекомендованная цена товара.
        category_id (str): Категория товара.
        ozon_name (str): Название товара на Озоне.
        name_1c (str): Название товара в 1С.
        wb_name (str): Название товара на WB.
        ozon_article (str): Артикул для Озона.
        wb_article (str): Артикул для WB.
        ym_article (str): Артикул для Яндекс.Маркета.
        wb_article_td (str): Артикул_ВБ_тд.

    Meta:
        verbose_name (str): Отображаемое имя в админке для одного объекта.
        verbose_name_plural (str): Отображаемое имя в админке
        для нескольких объектов.
    """
    id_product = models.CharField(
        verbose_name='ID товара',
        max_length=256,
        unique=True,
    )
    article = models.CharField(
        verbose_name='Артикул товара',
        max_length=256,
    )
    ean_13 = models.CharField(
        verbose_name='Код товара',
        max_length=15,
    )
    name = models.CharField(
        verbose_name='Название товара',
        max_length=256,
    )
    cost = models.CharField(
        verbose_name='Стоимость',
        max_length=256,
    )
    recommended_price = models.CharField(
        verbose_name='Рекомендованная цена',
        max_length=256,
    )
    category_id = models.CharField(
        verbose_name='Категория товара',
        max_length=256,
    )
    ozon_name = models.CharField(
        verbose_name='Название товара на Озоне',
        max_length=256,
    )
    name_1c = models.CharField(
        verbose_name='Название товара в 1С',
        max_length=256,
    )
    wb_name = models.CharField(
        verbose_name='Название товара на WB',
        max_length=256,
    )
    ozon_article = models.CharField(
        verbose_name='Артикул для Озон',
        max_length=256,
    )
    wb_article = models.CharField(
        verbose_name='Артикул для WB',
        max_length=256,
    )
    ym_article = models.CharField(
        verbose_name='Артикул для Яндекс.Маркета',
        max_length=256,
    )
    wb_article_td = models.CharField(
        verbose_name='Артикул_ВБ_тд',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Продукт Prosept'
        verbose_name_plural = 'Продукты Prosept'

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    """
    Модель, представляющая таблицу мэтчинга товаров Prosept и дилера.

    Attributes:
        key (DealerParsing): Связь с моделью DealerParsing, внешний
        ключ для связи с артикулом продукта дилера.
        product_id (Product): Связь с моделью Product, внешний
        ключ для связи с продуктом Prosept.
        dealer_id (Dealer): Связь с моделью Dealer, внешний
        ключ для связи с дилером.

    Meta:
        verbose_name (str): Отображаемое имя в админке для одного объекта.
        verbose_name_plural (str): Отображаемое имя в админке
        для нескольких объектов.
        unique_together (list): Список полей, которые должны
        быть уникальными в пределах модели.
    """
    key = models.ForeignKey(
        DealerParsing,
        verbose_name='Артикул продукта дилера',
        related_name='matches',
        to_field='product_key',
        on_delete=models.CASCADE,
    )
    product_id = models.ForeignKey(
        Product,
        verbose_name='Продукт Prosept',
        related_name='matches',
        to_field='id_product',
        on_delete=models.CASCADE,
    )
    dealer_id = models.ForeignKey(
        Dealer,
        verbose_name='Дилер',
        related_name='matches',
        to_field='id',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Связанный товар'
        verbose_name_plural = 'Связанные товары'
        unique_together = ('key', 'product_id', 'dealer_id')

    def __str__(self) -> str:
        return str(self.key)


class MatchingPredictions(models.Model):
    """
    Модель, представляющая возможное соответствие продуктов Prosept и дилера.

    Attributes:
        prosept_product_id (Product): Связь с моделью Product, внешний
        ключ для связи с совместимым продуктом Prosept.
        dealer_product_id (DealerParsing): Связь с моделью DealerParsing,
        внешний ключ для связи с продуктом дилера.

    Meta:
        verbose_name (str): Отображаемое имя в админке для одного объекта.
        verbose_name_plural (str): Отображаемое имя в админке для
        нескольких объектов.
        unique_together (list): Список полей, которые должны быть
        уникальными в пределах модели.
    """
    prosept_product_id = models.ForeignKey(
        Product,
        verbose_name='Совместимый продукт Prosept',
        related_name='predictions',
        to_field='id_product',
        on_delete=models.CASCADE,
    )
    dealer_product_id = models.ForeignKey(
        DealerParsing,
        verbose_name='Продукт Дилера',
        related_name='predictions',
        to_field='id',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Возможное соответствие'
        verbose_name_plural = 'Возможные соответствия'
        unique_together = ('prosept_product_id', 'dealer_product_id')

    def __str__(self) -> str:
        return f'{self.prosept_product_id} ->  {self.dealer_product_id}'
