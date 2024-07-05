# api/filters.py
import django_filters
from api.models.journal_models import JournalEntry

class JournalEntryFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="created_at__date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="created_at__date", lookup_expr='lte')

    class Meta:
        model = JournalEntry
        fields = ['title', 'id', 'start_date', 'end_date']
