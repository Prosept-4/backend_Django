import django_filters
from django.db.models import Exists, OuterRef

from products.models import DealerParsing, MatchingPredictions, Product


class DealerParsingFilter(django_filters.FilterSet):
    """
    Фильтр для объектов DealerParsing.

    Параметры:
        - min_date: Минимальная дата для фильтрации.
        - max_date: Максимальная дата для фильтрации.
        - is_matched: Фильтр по совпадениям.
        - is_postponed: Фильтр по отложенным товарам.
        - has_no_matches: Фильтр по товарам без совпадений.
        - is_analyzed: Фильтр по наличию предсказаний.

    Атрибуты:
        - model: Модель, к которой применяется фильтр.
        - fields: Поля, по которым можно выполнять фильтрацию.
    """
    min_date = django_filters.DateFilter(field_name='date', lookup_expr='gte',
                                         required=False)
    max_date = django_filters.DateFilter(field_name='date', lookup_expr='lte',
                                         required=False)
    is_matched = django_filters.BooleanFilter(field_name='is_matched',
                                              required=False)
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed',
                                                required=False)
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches',
                                                  required=False)
    is_analyzed = django_filters.BooleanFilter(method='filter_is_analyzed',
                                               label='Has Predictions',
                                               required=False)

    @staticmethod
    def filter_is_analyzed(queryset, name, value):
        """
        Метод для фильтрации по наличию предсказаний.

        Параметры:
            - queryset: Набор данных для фильтрации.
            - name: Имя фильтра.
            - value: Значение фильтра.

        Возвращает:
            - queryset: Отфильтрованный набор данных.
        """
        subquery = MatchingPredictions.objects.filter(
            dealer_product_id=OuterRef('product_key')
        ).values('dealer_product_id')[:1]

        return queryset.annotate(
            is_analyzed=Exists(subquery)
        ).filter(is_analyzed=value)


    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'is_matched', 'is_postponed',
                  'has_no_matches', 'is_analyzed']


class StatisticFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='date',
                                         lookup_expr='gte',
                                         required=False)
    max_date = django_filters.DateFilter(field_name='date',
                                         lookup_expr='lte',
                                         required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class DealerParsingIsPostponedFilter(django_filters.FilterSet):
    """
    Фильтр для объектов DealerParsing по отложенным товарам.

    Параметры:
        - min_date: Минимальная дата для фильтрации по отложенным товарам.
        - max_date: Максимальная дата для фильтрации по отложенным товарам.

    Атрибуты:
        - model: Модель, к которой применяется фильтр.
        - fields: Поля, по которым можно выполнять фильтрацию.
    """
    min_date = django_filters.DateFilter(field_name='postpone_date',
                                         lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='postpone_date',
                                         lookup_expr='lte', required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class DealerParsingHasNoMatchesFilter(django_filters.FilterSet):
    """
    Фильтр для объектов DealerParsing по товарам без совпадений.

    Параметры:
        - min_date: Минимальная дата для фильтрации по товарам без совпадений.
        - max_date: Максимальная дата для фильтрации по товарам без совпадений.

    Атрибуты:
        - model: Модель, к которой применяется фильтр.
        - fields: Поля, по которым можно выполнять фильтрацию.
    """
    min_date = django_filters.DateFilter(
        field_name='has_no_matches_toggle_date', lookup_expr='gte',
        required=False)
    max_date = django_filters.DateFilter(
        field_name='has_no_matches_toggle_date', lookup_expr='lte',
        required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class PredictionsFilter(django_filters.FilterSet):
    """
    Фильтр для объектов MatchingPredictions.

    Параметры:
        - dealer_product_id: Фильтр по идентификатору продукта дилера.

    Атрибуты:
        - model: Модель, к которой применяется фильтр.
        - fields: Поля, по которым можно выполнять фильтрацию.
    """
    dealer_product_id = django_filters.CharFilter(
        field_name='dealer_product_id', lookup_expr='exact')

    class Meta:
        model = MatchingPredictions
        fields = ['dealer_product_id']


class ProductFilter(django_filters.FilterSet):
    """
   Фильтр для объектов Product.

   Параметры:
       - name_1c: Фильтр по названию продукта в 1С.

   Атрибуты:
       - model: Модель, к которой применяется фильтр.
       - fields: Поля, по которым можно выполнять фильтрацию.
   """
    name_1c = django_filters.CharFilter(field_name='name_1c',
                                        lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name_1c']
