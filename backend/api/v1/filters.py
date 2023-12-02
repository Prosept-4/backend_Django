import django_filters

from products.models import DealerParsing


class DealerParsingFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='date', lookup_expr='lte', required=False)
    is_matched = django_filters.BooleanFilter(field_name='is_matched', required=False)
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed', required=False)
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches', required=False)
    

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'is_matched', 'is_postponed', 'has_no_matches']


class DealerParsingIsMatchedFilter(django_filters.FilterSet):
    # min_date = django_filters.DateFilter(field_name='matching_date', lookup_expr='gte', required=False)
    # max_date = django_filters.DateFilter(field_name='matching_date', lookup_expr='lte', required=False)
    is_matched = django_filters.BooleanFilter(field_name='is_matched', required=False)
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed', required=False)
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches', required=False)

    class Meta:
        model = DealerParsing
        fields = ['is_matched']


class DealerParsingIsPostponedFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='postpone_date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='postpone_date', lookup_expr='lte', required=False)
    is_postponed = django_filters.BooleanFilter(field_name='is_postponed', required=False)

    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'is_postponed']


class DealerParsingHasNoMatchesFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name='has_no_matches_toggle_date', lookup_expr='gte', required=False)
    max_date = django_filters.DateFilter(field_name='has_no_matches_toggle_date', lookup_expr='lte', required=False)
    has_no_matches = django_filters.BooleanFilter(field_name='has_no_matches', required=False)


    class Meta:
        model = DealerParsing
        fields = ['min_date', 'max_date', 'has_no_matches']