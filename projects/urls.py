from django.urls import path, include
from .views import ProjectListCreateView, ProjectDetailView, MyTokenObtainPairView, MyTokenRefreshView, RewardViewSet,PledgeViewSet
from rest_framework.routers import DefaultRouter
from .views import my_projects, my_backings, my_profile
from .views import PetitionViewSet, user_profile_view, check_username
# from .views import EventViewSet







router = DefaultRouter()
router.register(r'rewards', RewardViewSet, basename='reward')
router.register(r'pledges', PledgeViewSet, basename='pledge')
router.register(r'petitions', PetitionViewSet, basename='petition')
# router.register(r'events', EventViewSet, basename='events')


urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),  # 👈 This adds the /rewards/and /pledges/ endpoints

]
urlpatterns += [
    path("my-projects/", my_projects, name='my-projects'),
    path("my-backings/", my_backings, name='my-backings'),
    path("me/", my_profile, name='my-profile'),
    path('edit-profile/', user_profile_view, name='edit-profile'),
    path('check-username/', check_username, name='check-username'),
]

# urlpatterns += router.urls
