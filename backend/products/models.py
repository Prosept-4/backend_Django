from django.db import models


class Dealer(models.Model):
    """Список дилеров"""
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


class Price(models.Model):
    """Результат работы парсера площадок дилеров"""
    product_key = models.CharField(
        verbose_name='Уникальный номер позиции',
        max_length=256,
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
    date = models.DateTimeField(
        verbose_name='Дата получения информации',
        max_length=256,
    )
    dealer_id = models.CharField(
        verbose_name='Идентефикатор дилера',
        max_length=256,
    )
    is_match = models.BooleanField(
        default=False,
    )
    coincidence = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Цена дилера'
        verbose_name_plural = 'Цены дилеров'

    def __str__(self) -> str:
        return self.key


class Product(models.Model):
    """Список товаров, которые производит и распостранят заказчик"""
    id_product = models.CharField(
        verbose_name='ID товара',
        max_length=256,
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
        verbose_name='Название товара на Вайлдберриз',
        max_length=256,
    )
    ozon_article = models.CharField(
        verbose_name='Артикул для Озон',
        max_length=256,
    )
    wb_article = models.CharField(
        verbose_name='Артикул для Вайлберриз',
        max_length=256,
    )
    ym_article = models.CharField(
        verbose_name='артикул для Яндекс.Маркета',
        max_length=256,
    )
    wb_article_td = models.CharField(
        verbose_name='Артикул_ВБ_тд',
        max_length=256,
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return self.name


class Match(models.Model):
    """Таблица мэтчинга товаров заказчика и дилера"""
    # Внешний ключ к Price
    key = models.ForeignKey(
        Price,
        verbose_name='Цена',
        related_name='product',
        on_delete=models.CASCADE,
    )
    # Внешний ключ к Product
    dealer_id = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='product',
        on_delete=models.CASCADE,
    )
    # Внешний ключ к Dealer
    product_id = models.ForeignKey(
        Dealer,
        verbose_name='Дилер',
        related_name='dealer',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Товар дилера'
        verbose_name_plural = 'Товары дилера'

    def __str__(self) -> str:
        return self.key
