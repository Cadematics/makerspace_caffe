from django.contrib import admin
from .models import Project  # Ensure you import the correct model
from .models import Reward

admin.site.register(Project)  # Correct model name (singular)

admin.site.register(Reward)  # Correct model name (singular)
