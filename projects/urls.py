from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, MyTokenObtainPairView, MyTokenRefreshView


urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
