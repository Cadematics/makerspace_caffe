from django.urls import path
from .views import EventListView, buy_ticket, my_tickets,EventDetailView
from .views import purchase_ticket, create_checkout_session, stripe_webhook


urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/buy-ticket/', buy_ticket, name='buy-ticket'),
    path('purchase-ticket/', buy_ticket, name='purchase-ticket'),
    path('my-tickets/', my_tickets, name='my-tickets'),
    path('events/create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    
    path('stripe/webhook', stripe_webhook, name='stripe-webhook'),  # no slash
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook-slash'),  # with slash


]

