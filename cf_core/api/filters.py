import django_filters
from .. import models


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class ModerationNotesFilter(django_filters.FilterSet):

    is_new = django_filters.BooleanFilter(method='get_newest')

    def get_newest(self, queryset, name, value):
        return queryset.filter(last_seen__isnull=value)

    class Meta:
        model = models.ModerationNote
        fields = ('content_type', 'object_id', 'is_new')
