
from rest_framework import serializers
from .models import Event




class EventSerializer(serializers.ModelSerializer):
    is_ticketed = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title',
            'start_datetime', 'end_datetime', 
            'location', 'photo', 'cost',
            'number_of_tickets', 'tickets_sold',
            'discount', 'description',
            'is_ticketed'
        ]

    def get_is_ticketed(self, obj):
        return obj.tickets_sold > 0
