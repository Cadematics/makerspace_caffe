
from rest_framework import serializers
from .models import Event, TicketPurchase

from .models import CrowdfundingEvent
from projects.serializers import RewardSerializer


from rest_framework import serializers
from .models import Event, TicketPurchase, CrowdfundingEvent
from projects.serializers import RewardSerializer



class CrowdfundingEventSerializer(serializers.ModelSerializer):
    rewards = RewardSerializer(many=True, read_only=True, source='crowdfunding_rewards')

    class Meta:
        model = CrowdfundingEvent
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'goal_amount', 'current_funding', 'photo', 'rewards']


class EventSerializer(serializers.ModelSerializer):
    is_ticketed = serializers.SerializerMethodField()
    photo = serializers.ImageField(use_url=True, required=False)
    rewards = RewardSerializer(many=True, read_only=True, source='event_rewards')

    class Meta:
        model = Event
        fields = [
            'id', 'title',
            'start_datetime', 'end_datetime',
            'location', 'photo', 'cost',
            'number_of_tickets', 'tickets_sold',
            'discount', 'description',
            'is_ticketed', 'rewards'
        ]

    def get_is_ticketed(self, obj):
        return obj.tickets_sold > 0


class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = ['id', 'user', 'event', 'quantity', 'purchased_at']
        read_only_fields = ['user', 'purchased_at']
