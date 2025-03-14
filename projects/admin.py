from django.contrib import admin
from .models import Project  # Ensure you import the correct model

admin.site.register(Project)  # Correct model name (singular)
