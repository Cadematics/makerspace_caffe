from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # ensure this is included
    class Meta:
        model = Project
        fields = '__all__'


