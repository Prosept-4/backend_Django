import django_filters

from products.models import DealerParsing


class DealerParsingFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date']


class DealerParsingStatisticFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', required=False)
    is_matched = django_filters.BooleanFilter(field_name='is_matched', required=False)
    # matching_date = django_filters.DateField()
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed', required=False)
    # postpone_date = django_filters.DateField()
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches', required=False)
    # has_no_matches_toggle_date = django_filters.DateField()

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'is_matched']