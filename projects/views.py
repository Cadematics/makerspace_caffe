from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import serializers, status, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

 
from .models import Reward, Project, Pledge, Petition
from .serializers import RewardSerializer, ProjectSerializer, PledgeSerializer, PetitionSerializer

import requests
from django.conf import settings

from .models import UserProfile
from .serializers import UserProfileSerializer



# Create your views here.

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])  # for avatar image upload
def user_profile_view(request):
    print('user profile request', request)
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'GET':
        user_data = UserSerializer(user).data
        profile_data = UserProfileSerializer(profile, context={'request': request}).data
        combined_data = {**user_data, **profile_data}
        return Response(combined_data)

    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        profile_serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user_serializer.save()
            profile_serializer.save()
            combined_data = {**user_serializer.data, **profile_serializer.data}
            return Response(combined_data)

        errors = {
            'user_errors': user_serializer.errors,
            'profile_errors': profile_serializer.errors,
        }
        return Response(errors, status=400)


# views.py
@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request):
    username = request.query_params.get('username')
    if not username:
        return Response({'error': 'Username is required'}, status=400)

    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})




class PetitionViewSet(viewsets.ModelViewSet):
    queryset = Petition.objects.all()
    serializer_class = PetitionSerializer

    def create(self, request, *args, **kwargs):
        print("📨 POST DATA:", request.data)

        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ Petition validation error:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = request.data.get('street', '') + ", " + request.data.get('city', '') + ", " + request.data.get('state', '') + " " + request.data.get('zip_code', '')
        lat, lng = 0.0, 0.0

        if address.strip():
            key = settings.OPENCAGE_API_KEY
            url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={key}"
            try:
                response = requests.get(url)
                data = response.json()
                if data.get('results'):
                    coords = data['results'][0]['geometry']
                    lat, lng = coords['lat'], coords['lng']
            except Exception as e:
                print("⚠️ Geocoding failed:", e)

        serializer.save(lat=lat, lng=lng)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    user = request.user
    projects = Project.objects.filter(authauthor=user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_backings(request):
    user = request.user
    pledges = Pledge.objects.filter(user=user).select_related('project', 'reward')
    data = [
        {
            "backing_id": pledge.id,
            "project_title": pledge.project.title,
            "amount": pledge.amount,
            "reward": pledge.reward.title if pledge.reward else "No reward",
        }
        for pledge in pledges
    ]
    return Response(data)



# API endpoint for listing and creating projects
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# API endpoint for retrieving, updating, and deleting a single project
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer



# View to get the access and refresh tokens
class MyTokenObtainPairView(TokenObtainPairView):
    pass

# View to refresh the token
class MyTokenRefreshView(TokenRefreshView):
    pass



# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# projects/views.py
class RewardViewSet(viewsets.ModelViewSet):
    serializer_class = RewardSerializer

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Reward.objects.filter(project_id=project_id)
        return Reward.objects.all()



class PledgeViewSet(viewsets.ModelViewSet):
    queryset = Pledge.objects.all()
    serializer_class = PledgeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        pledge = serializer.save(user=self.request.user)

        # Add the pledged amount to the project's current funding
        project = pledge.project
        project.current_funding += pledge.amount
        project.save()



