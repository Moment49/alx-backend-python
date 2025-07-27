import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.CharFilter(field_name='conversation__participants__user_id', lookup_expr='exact', required=False)
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    class Meta:
        model = Message
        fields = ['conversation', 'sent_before', 'sent_after']