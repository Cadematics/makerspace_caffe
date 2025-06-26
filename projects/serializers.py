from rest_framework import serializers
from .models import Project
from .models import Reward
from .models import Pledge
from .models import Petition
from .models import User
from .models import UserProfile




class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    author_name = serializers.CharField(source='authauthor.username', read_only=True)
    backers_count = serializers.SerializerMethodField()  # 👈 Add this

    class Meta:
        model = Project
        fields = '__all__'  # Or list out fields manually
        # e.g., fields = ['id', 'title', ..., 'backers_count']

    def get_backers_count(self, obj):
        return obj.pledge_set.values('user').distinct().count()


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'


class PledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pledge
        fields = '__all__'
        read_only_fields = ['user']


class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = ['id', 'name', 'street', 'city', 'state', 'zip_code', 'message',
                   'lat', 'lng',
                     'created_at']
        # fields = '__all__'
        read_only_fields = ['lat', 'lng', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'avatar']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']
    
    def get_avatar(self, obj):
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url)
        return None
    
