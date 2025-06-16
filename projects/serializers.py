from rest_framework import serializers
from .models import Project
from .models import Reward

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # ensure this is included
    class Meta:
        model = Project
        fields = '__all__'



class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'