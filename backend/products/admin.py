from django.contrib import admin

from .models import (Dealer,
                     Price,
                     Product,
                     Match)


class DealerAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name'
    )


class PriceAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'product_key',
        'price',
        'product_url',
        'product_name',
        'date',
        'dealer_id',
        'is_match',
        'coincidence',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
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


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'key',
        'dealer_id',
        'product_id',
    )


admin.site.register(Dealer, DealerAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Match, MatchAdmin)