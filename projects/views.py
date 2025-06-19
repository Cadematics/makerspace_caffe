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





from .serializers import PetitionSerializer

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






# class PetitionViewSet(viewsets.ModelViewSet):
#     queryset = Petition.objects.all()
#     serializer_class = PetitionSerializer

#     def perform_create(self, serializer):
#         address = self.request.data.get('address')
#         if address:
#             key = settings.OPENCAGE_API_KEY
#             url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={key}"
#             response = requests.get(url)
#             data = response.json()

#             if data['results']:
#                 coords = data['results'][0]['geometry']
#                 serializer.save(lat=coords['lat'], lng=coords['lng'])
#                 return
#         # fallback if no geocode
#         serializer.save(lat=0.0, lng=0.0)

#     def create(self, request, *args, **kwargs):
#         print("POST DATA:", request.data)
#         return super().create(request, *args, **kwargs)










# class PetitionViewSet(viewsets.ModelViewSet):
#     queryset = Petition.objects.all().order_by('-created_at')
#     serializer_class = PetitionSerializer




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_created_projects(request):
    user = request.user
    projects = Project.objects.filter(authauthor=user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)







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




# class RewardViewSet(viewsets.ModelViewSet):
#     queryset = Reward.objects.all()
#     serializer_class = RewardSerializer


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



