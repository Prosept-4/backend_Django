from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from products.models import (Dealer, DealerParsing, Product,
                             Match, MatchingPredictions)


class DealerAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name'
    )


class DealerParsingAdmin(ImportExportModelAdmin):
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
        'matching_date',
        'has_no_matches_toggle_date',
    )


class ProductAdmin(ImportExportModelAdmin):
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
    list_display = (
        'id',
        'key',
        'dealer_id',
        'product_id',
    )


class MatchingPredictionsAdmin(admin.ModelAdmin):
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
