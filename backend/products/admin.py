from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from products.models import (Dealer, DealerParsing, Product,
                             Match, MatchingPredictions)


class DealerAdmin(ImportExportModelAdmin):
    """
    Admin класс для модели Dealer.

    Атрибуты:
        - list_display: Список полей для отображения в списке объектов.
    """
    list_display = (
        'id',
        'name'
    )


class DealerParsingAdmin(ImportExportModelAdmin):
    """
    Admin класс для модели DealerParsing.

    Атрибуты:
        - list_display: Список полей для отображения в списке объектов.
    """
    list_display = (
        'id',
        'product_key',
        'price',
        'product_url',
        'product_name',
        'date',
        'dealer_id',
        'is_matched',
        'has_no_matches',
        'is_postponed',
        'postpone_date',
        'matching_date',
        'has_no_matches_toggle_date',
    )


class ProductAdmin(ImportExportModelAdmin):
    """
    Admin класс для модели Product.

    Атрибуты:
        - list_display: Список полей для отображения в списке объектов.
    """
    list_display = (
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


class MatchAdmin(ImportExportModelAdmin):
    """
    Admin класс для модели Match.

    Атрибуты:
        - list_display: Список полей для отображения в списке объектов.
    """
    list_display = (
        'id',
        'key',
        'dealer_id',
        'product_id',
    )


class MatchingPredictionsAdmin(admin.ModelAdmin):
    """
    Admin класс для модели MatchingPredictions.

    Атрибуты:
        - list_display: Список полей для отображения в списке объектов.
    """
    list_display = (
        'id',
        'prosept_product_id',
        'dealer_product_id',
    )


admin.site.register(Dealer, DealerAdmin)
admin.site.register(DealerParsing, DealerParsingAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(MatchingPredictions, MatchingPredictionsAdmin)
