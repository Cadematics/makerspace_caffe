from django.shortcuts import render

# Create your views here.



from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer

# API endpoint for listing and creating projects
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# API endpoint for retrieving, updating, and deleting a single project
class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
