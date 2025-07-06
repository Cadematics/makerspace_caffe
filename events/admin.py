from django.contrib import admin
from .models import Event, TicketPurchase, CrowdfundingEvent

# Register your models here.

# admin.site.register(TicketPurchase)

@admin.register(TicketPurchase)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'quantity', 'purchased_at')



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'end_datetime', 'is_ticketed')
    ordering = ('start_datetime',)

    @admin.display(boolean=True, description='Ticketed')
    def is_ticketed(self, obj):
        return obj.tickets_sold > 0


@admin.register(CrowdfundingEvent)
class CrowdfundingEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')

