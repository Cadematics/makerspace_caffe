from django.shortcuts import render
from rest_framework import generics
from .serializers import EventSerializer
from rest_framework.permissions import AllowAny

from .models import CrowdfundingEvent
from .serializers import CrowdfundingEventSerializer




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Event, TicketPurchase
from .serializers import TicketPurchaseSerializer

from rest_framework.generics import RetrieveAPIView
from .serializers import EventSerializer

import stripe
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json

from django.contrib.auth import get_user_model


# Create your views here.

User = get_user_model()

def handle_checkout_session(session):
    print("\n✅ Stripe webhook session received:")
    print(json.dumps(session, indent=2))

    # 1️⃣ Extract metadata
    metadata = session.get('metadata', {})
    event_id = metadata.get('event_id')
    quantity = int(metadata.get('quantity', 1))

    # Defensive: Check event_id
    if not event_id:
        print("❌ ERROR: No event_id in metadata!")
        return

    # 2️⃣ Extract customer email
    customer_details = session.get('customer_details', {})
    customer_email = customer_details.get('email')

    if not customer_email:
        print("❌ ERROR: No customer email in session!")
        return

    print(f"🟢 Parsed from Stripe: event_id={event_id}, quantity={quantity}, email={customer_email}")

    # 3️⃣ Look up Event
    try:
        event_obj = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        print(f"❌ ERROR: Event with id={event_id} not found.")
        return

    # 4️⃣ Look up User
    try:
        user_obj = User.objects.get(email=customer_email)
    except User.DoesNotExist:
        print(f"❌ ERROR: User with email={customer_email} not found.")
        return

    # 5️⃣ Create TicketPurchase
    TicketPurchase.objects.create(
        user=user_obj,
        event=event_obj,
        quantity=quantity
    )

    # 6️⃣ Increment event.tickets_sold
    event_obj.tickets_sold += quantity
    event_obj.save()

    print(f"✅ SUCCESS: Created TicketPurchase for {user_obj.email} for event '{event_obj.title}' with quantity={quantity}")




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # ✅ Handle the event
    if event['type'] == 'checkout.session.completed':
        print('event', event)
        session = event['data']['object']
        handle_checkout_session(session)

    return HttpResponse(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    try:
        quantity = int(request.data.get('quantity', 1))
        event_id = request.data.get('event')
        # Fetch event details from DB
        event = Event.objects.get(id=event_id)

        YOUR_DOMAIN = "http://localhost:3000"  # or 5173 or your frontend URL

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': event.title,
                    },
                    'unit_amount': int(event.cost * 100),
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
            client_reference_id=str(request.user.id),
            metadata={
                'event_id': str(event.id),
                'quantity': str(quantity),
            }
        )

        return Response({'sessionId': checkout_session.id})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_tickets(request):
    user = request.user
    tickets = TicketPurchase.objects.filter(user=user).select_related('event')
    data = [
        {
            "id": ticket.id,
            "event_id": ticket.event.id,
            "event_title": ticket.event.title,
            "event_photo": request.build_absolute_uri(ticket.event.photo.url) if ticket.event.photo else None,
            "quantity": ticket.quantity,
        }
        for ticket in tickets
    ]
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def buy_ticket(request):
    user = request.user
    event_id = request.data.get('event')
    quantity = int(request.data.get('quantity', 1))

    if not event_id:
        return Response({"error": "Event ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

    # Check if enough tickets
    if (event.number_of_tickets - event.tickets_sold) < quantity:
        return Response({"error": "Not enough tickets left."}, status=status.HTTP_400_BAD_REQUEST)

    # Record purchase
    purchase = TicketPurchase.objects.create(user=user, event=event, quantity=quantity)
    event.tickets_sold += quantity
    event.save()

    serializer = TicketPurchaseSerializer(purchase)
    return Response(serializer.data, status=status.HTTP_201_CREATED)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_ticket(request):
    data = request.data.copy()
    data['user'] = request.user.id
    serializer = TicketPurchaseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        # Optionally: decrement available tickets on the event
        event = serializer.validated_data['event']
        event.tickets_sold += serializer.validated_data['quantity']
        event.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]





class CrowdfundingEventListView(generics.ListAPIView):
    queryset = CrowdfundingEvent.objects.all()
    serializer_class = CrowdfundingEventSerializer
    permission_classes = [AllowAny]


class CrowdfundingEventDetailView(generics.RetrieveAPIView):
    queryset = CrowdfundingEvent.objects.all()
    serializer_class = CrowdfundingEventSerializer
    permission_classes = [AllowAny]
