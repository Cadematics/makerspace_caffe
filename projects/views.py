from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from .models import Reward
from .serializers import RewardSerializer

from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

from .models import Pledge
from .serializers import PledgeSerializer


from .models import Petition
from .serializers import PetitionSerializer

import requests
from django.conf import settings



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_profile(request):
#     user = request.user
#     data = {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "name": user.first_name + " " + user.last_name,
#         "bio": "",  # Add `bio` if you're storing it somewhere
#         "avatar": "",  # Add `avatar` if applicable
#     }
#     return Response(data)



@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)







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




# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def my_backings(request):
#     user = request.user
#     pledges = Pledge.objects.filter(user=user).select_related("project")
#     backed_projects = [pledge.project for pledge in pledges]
#     serializer = ProjectSerializer(backed_projects, many=True)
#     return Response(serializer.data)




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





# Create your views here.

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



