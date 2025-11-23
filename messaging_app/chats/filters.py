from django_filters import rest_framework as filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(filters.FilterSet):
    sender = filters.ModelChoiceFilter(queryset=User.objects.all())

    recipient = filters.ModelChoiceFilter(queryset=User.objects.all())

    start_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']
