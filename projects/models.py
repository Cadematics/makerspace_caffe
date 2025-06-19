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

# class Reward(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rewards')
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     minimum_pledge = models.DecimalField(max_digits=10, decimal_places=2)



class Reward(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='rewards')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='reward_images/', null=True, blank=True)  # new
    estimated_delivery = models.DateField(null=True, blank=True)  # new
    ships_to = models.CharField(max_length=255, default="Anywhere in the world")  # new
    quantity_limit = models.IntegerField(null=True, blank=True)  # new
    backer_count = models.IntegerField(default=0)  # new
    items_included = models.TextField(blank=True)  # new

    def __str__(self):
        return f"{self.title} - ${self.amount}"
    


class Pledge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class PetitionSignature(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    # lat = models.FloatField(null=True, blank=True)
    # lng = models.FloatField(null=True, blank=True)
    signed_at = models.DateTimeField(auto_now_add=True)



class Petition(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    lat = models.FloatField(default=0.0)  # ✅ Add this
    lng = models.FloatField(default=0.0)  # ✅ And this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} from {self.city}, {self.state}"
  
  
  
  
  
  
    # lat = models.FloatField(null=True)
    # lng = models.FloatField(null=True)