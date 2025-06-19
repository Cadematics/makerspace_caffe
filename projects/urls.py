from django.urls import path, include
from .views import ProjectListCreateView, ProjectDetailView, MyTokenObtainPairView, MyTokenRefreshView, RewardViewSet,PledgeViewSet
from rest_framework.routers import DefaultRouter
from .views import my_created_projects
from .views import PetitionViewSet



router = DefaultRouter()
router.register(r'rewards', RewardViewSet, basename='reward')
router.register(r'pledges', PledgeViewSet)
router.register(r'petitions', PetitionViewSet, basename='petition')



urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # 👈 This adds the /rewards/and /pledges/ endpoints

]





urlpatterns += [
    path('my-created-projects/', my_created_projects, name='my-created-projects'),
]