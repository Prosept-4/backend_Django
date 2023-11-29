from rest_framework import serializers


from products.models import Dealer, Price, Product, Match


class DealerSerializer(serializers.ModelSerializer):
    """Сериализатор отображения списка дилеров"""

class Meta:
    model = Dealer
    fields = (
        'id',
        'name'
    )


class PriceSerializer(serializers.ModelSerializer):
    """Сериализатор отображения списка цен дилеров"""

class Meta:
    model = Price
    fields = (
        'id',
        'product_key',
        'price',
        'product_url',
        'product_name',
        'date',
        'dealer_id',
        'is_match',
        'coincidence',
    )


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор отображения списка продуктов"""

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
    """Сериализатор отображения списка мэтчей"""

class Meta:
    model = Match
    fields = (
        'id,'
        'key',
        'dealer_id',
        'product_id',
    )