from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    funding_goal = models.DecimalField(max_digits=10, decimal_places=2)
    current_funding = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # ✅ New fields
    # image = models.URLField(blank=True, null=True)  # or use ImageField if uploading
    image = models.ImageField(upload_to="project_images/", null=True, blank=True)

    authauthor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=100, default="Design")
    location = models.CharField(max_length=100, default="San Francisco, CA")
    deadline = models.DateField(default=date.today)  
    

    def days_left(self):
        return (self.deadline - date.today()).days

    def funding_percent(self):
        return round((self.current_funding / self.funding_goal) * 100) if self.funding_goal > 0 else 0

    def __str__(self):
        return self.title
