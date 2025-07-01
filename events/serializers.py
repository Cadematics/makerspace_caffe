
from rest_framework import serializers
from .models import Event, TicketPurchase



class EventSerializer(serializers.ModelSerializer):
    is_ticketed = serializers.SerializerMethodField()
    photo = serializers.ImageField(use_url=True, required=False)

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


class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = ['id', 'user', 'event', 'quantity', 'purchased_at']
        read_only_fields = ['user','purchased_at']
