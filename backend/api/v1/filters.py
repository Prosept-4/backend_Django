import django_filters
from django.db.models import Exists, OuterRef

from products.models import DealerParsing, MatchingPredictions, Match


class DealerParsingFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', required=False)
    is_matched = django_filters.BooleanFilter(field_name='is_matched', required=False)
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed', required=False)
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches', required=False)
    is_analyzed = django_filters.BooleanFilter(method='filter_is_analyzed', label='Has Predictions')

    @staticmethod
    def filter_is_analyzed(queryset, name, value):
        subquery = MatchingPredictions.objects.filter(
            dealer_product_id=OuterRef('id')
        ).values('dealer_product_id')[:1]

        return queryset.annotate(
            is_analyzed=Exists(subquery)
        ).filter(is_analyzed=value)
    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'is_matched', 'is_postponed',
                  'has_no_matches', 'is_analyzed']


class DealerParsingIsMatchedFilter(django_filters.FilterSet):
    pass
#     min_date = django_filters.DateFilter(field_name='key__matching_date', lookup_expr='gte', required=False)
#     max_date = django_filters.DateFilter(field_name='key__matching_date', lookup_expr='lte', required=False)

#     class Meta:
#         model = Match
#         fields = ['min_date', 'max_date']


class DealerParsingIsPostponedFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='postpone_date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='postpone_date', lookup_expr='lte', required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class DealerParsingHasNoMatchesFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='has_no_matches_toggle_date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='has_no_matches_toggle_date', lookup_expr='lte', required=False)
 


    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class PredictionsFilter(django_filters.FilterSet):
    dealer_product_id = django_filters.NumberFilter(field_name='dealer_product_id', lookup_expr='exact')

    class Meta:
        model = MatchingPredictions
        fields = ['dealer_product_id']