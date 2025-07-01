from django.db import models
import datetime 
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.








class Event(models.Model):
    title = models.CharField(max_length=255)
    start_datetime = models.DateField(default="2025-06-01")
    end_datetime = models.DateField(default="2025-06-02")
    location = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to="event_photos/", blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    number_of_tickets = models.IntegerField(default=0)
    tickets_sold = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)

    def tickets_left(self):
        return self.number_of_tickets - self.tickets_sold

    def __str__(self):
        return self.title



class TicketPurchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.quantity})"


