from django.shortcuts import render
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import AllowAny

# Create your views here.


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

