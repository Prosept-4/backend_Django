from datetime import datetime

from rest_framework import serializers

from products.models import (Dealer, DealerParsing, Product,
                             Match, MatchingPredictions)


class DealerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка дилеров.

    Атрибуты класса:
        - model: Модель, используемая для сериализации;
        - fields: Список полей модели, которые будут сериализованы.
    """

    class Meta:
        model = Dealer
        fields = (
            'id',
            'name'
        )


class DealerParsingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения спарсенного списка товаров дилеров.

    Методы:
        - to_representation: Преобразует данные DealerParsing
            для представления в JSON.
    """
    def to_representation(self, instance):
        """
        Преобразует данные DealerParsing для представления в JSON.

        Аргументы:
            - `instance`: экземпляр модели, который нужно сериализовать.

        Возвращает:
            - `dict`: словарь с данными для представления.
        """
        representation = super().to_representation(instance)

        dealer = instance.dealer_id

        representation['dealer_name'] = dealer.name

        return representation

    class Meta:
        model = DealerParsing
        fields = (
            'id',
            'product_key',
            'price',
            'product_url',
            'product_name',
            'date',
            'dealer_id',
            'is_matched',
            'matching_date',
            'is_postponed',
            'postpone_date',
            'has_no_matches',
            'has_no_matches_toggle_date',
        )


class DealerParsingPostponeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения и обновления отложенных
    элементов DealerParsing.

    Позволяет преобразовывать данные отложенных элементов для отображения
    и выполнения обновления.

    Атрибуты класса:
        - `model`: модель, используемая для сериализации;
        - `fields`: список полей модели, которые будут сериализованы.

    Методы:
        - `update`: обновляет данные отложенного элемента.
    """

    def to_representation(self, instance):
        """
        Преобразует данные отложенного элемента для представления в JSON.

        Аргументы:
        - `instance`: экземпляр модели, который нужно сериализовать.

        Возвращает:
        - `dict`: словарь с данными для представления.

        Пример использования:
        ```
        to_representation(instance)
        """
        representation = super().to_representation(instance)
        representation['product_name'] = instance.product_name
        representation['product_key'] = instance.product_key
        representation['postpone_date'] = instance.postpone_date
        representation['product_url'] = instance.product_url
        representation['price'] = instance.price

        return representation

    def update(self, instance, validated_data):
        """
        Обновляет данные отложенного элемента.

        Аргументы:
            - `instance`: экземпляр модели, который нужно обновить;
            - `validated_data`: словарь с проверенными данными для обновления.

        Возвращает:
            - `instance`: обновленный экземпляр модели.
        """
        instance.is_postponed = validated_data.get('is_postponed',
                                                   instance.is_postponed)
        # Если убираем состояние "Отложено" - убираем и дату.
        if instance.is_postponed is False:
            instance.postpone_date = None
        else:
            instance.postpone_date = datetime.now().strftime("%Y-%m-%d")

        instance.is_matched = False
        instance.matching_date = None
        instance.has_no_matches = False
        instance.has_no_matches_toggle_date = None

        instance.save()
        return instance

    class Meta:
        model = DealerParsing
        fields = (
            'id',
            'is_postponed',
        )


class DealerParsingNoMatchesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения и обновления элементов
    DealerParsing без соответствий.

    Позволяет преобразовывать данные элементов без соответствий для
    отображения и выполнения обновления.

    Атрибуты класса:
        - `model`: модель, используемая для сериализации;
        - `fields`: список полей модели, которые будут сериализованы.

    Методы:
        - `update`: обновляет данные элемента без соответствий.
    """

    def to_representation(self, instance):
        """
        Преобразует данные элемента без соответствий для представления в JSON.

        Аргументы:
            - `instance`: экземпляр модели, который нужно сериализовать.

        Возвращает:
            - `dict`: словарь с данными для представления.
        """
        representation = super().to_representation(instance)
        representation['product_name'] = instance.product_name
        representation['product_key'] = instance.product_key
        representation[
            'has_no_matches_toggle_date'] = instance.has_no_matches_toggle_date
        representation['product_url'] = instance.product_url
        representation['price'] = instance.price
        return representation

    def update(self, instance, validated_data):
        """
        Обновляет данные элемента без соответствий.

        Аргументы:
            - `instance`: экземпляр модели, который нужно обновить;
            - `validated_data`: словарь с проверенными данными для обновления.

        Возвращает:
            - `instance`: обновленный экземпляр модели.
        """
        instance.has_no_matches = validated_data.get('has_no_matches',
                                                     instance.has_no_matches)
        # Если убираем состояние "Нет совпадений" - убираем и дату.
        if instance.has_no_matches is False:
            instance.has_no_matches_toggle_date = None
        else:
            instance.has_no_matches_toggle_date = datetime.now().strftime(
                "%Y-%m-%d")

        instance.is_postponed = False
        instance.postpone_date = None
        instance.is_matched = False
        instance.matching_date = None

        instance.save()
        return instance

    class Meta:
        model = DealerParsing
        fields = (
            'id',
            'has_no_matches',
        )


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка продуктов.

    Атрибуты класса:
        - model: Модель, используемая для сериализации;
        - fields: Список полей модели, которые будут сериализованы.
    """

    class Meta:
        model = Product
        fields = (
            'id',
            'id_product',
            'article',
            'ean_13',
            'name',
            'cost',
            'recommended_price',
            'category_id',
            'ozon_name',
            'name_1c',
            'wb_name',
            'ozon_article',
            'wb_article',
            'ym_article',
            'wb_article_td',
        )


class MatchSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка мэтчей.

    Методы:
        - to_representation: Преобразует данные мэтча для представления в JSON.
    """

    def to_representation(self, instance):
        """
        Преобразует данные мэтча для представления в JSON.

        Параметры:
            - instance: Экземпляр модели, который нужно сериализовать.

        Возвращает:
            - dict: Словарь с данными для представления.
        """
        representation = super().to_representation(instance)

        # Получаем связанный объект DealerParsing
        dealer_parsing = instance.key
        prosept_product = instance.product_id

        # Добавляем необходимые поля из связанного объекта
        # DealerParsing и Dealer.
        representation['dealer_name'] = dealer_parsing.dealer_id.name
        representation['dealer_product_name'] = dealer_parsing.product_name
        representation['dealer_product_price'] = dealer_parsing.price
        representation['dealer_product_url'] = dealer_parsing.product_url
        representation['matching_date'] = dealer_parsing.matching_date
        representation['prosept_name_1c'] = prosept_product.name_1c
        representation['prosept_name'] = prosept_product.name
        representation['prosept_article'] = prosept_product.article
        representation['prosept_cost'] = prosept_product.cost

        return representation

    class Meta:
        model = Match
        fields = (
            'id',
            'key',
            'dealer_id',
            'product_id',
        )


class MatchPartialUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для частичного обновления мэтча.

    Метод:
        - update: Обновляет данные мэтча.
    """

    def update(self, instance, validated_data):
        """
        Обновляет данные мэтча.

        Параметры:
            - instance: Экземпляр модели, который нужно обновить.
            - validated_data: Словарь с проверенными данными для обновления.

        Возвращает:
            - instance: Обновленный экземпляр модели.
        """
        # Обновляем данные
        instance.key = validated_data.get('key', instance.key)
        if instance.key.is_matched is False:
            instance.key.matching_date = None
        else:
            instance.key.matching_date = datetime.now().strftime("%Y-%m-%d")
        instance.key.is_postponed = False
        instance.key.postpone_date = None
        instance.key.has_no_matches = False
        instance.key.has_no_matches_toggle_date = None

        instance.save()
        return instance

    class Meta:
        model = Match
        fields = ['key', 'dealer_id', 'product_id']


class MatchingPredictionsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка предсказаний совпадений.

    Метод:
        - to_representation: Преобразует данные предсказания для
            представления в JSON.
    """
    def to_representation(self, instance):
        """
        Преобразует данные предсказания для представления в JSON.

        Параметры:
            - instance: Экземпляр модели, который нужно сериализовать.

        Возвращает:
            - dict: Словарь с данными для представления.
        """
        representation = super().to_representation(instance)

        # Получаем связанный объект DealerParsing и Products.
        dealer_parsing = instance.dealer_product_id
        prosept_product = instance.prosept_product_id

        # Добавляем необходимые поля из связанного
        #  объекта DealerParsing и Dealer.
        representation['dealer_name'] = dealer_parsing.dealer_id.name
        representation['product_name'] = dealer_parsing.product_name
        representation['product_url'] = dealer_parsing.product_url
        representation['name_1c'] = prosept_product.name_1c
        representation['name'] = prosept_product.name
        representation['id_product'] = prosept_product.id_product
        representation['article'] = prosept_product.article
        representation['recommended_price'] = prosept_product.cost

        return representation

    class Meta:
        model = MatchingPredictions
        fields = '__all__'
