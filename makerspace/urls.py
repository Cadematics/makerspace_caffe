
from django.contrib import admin
from django.urls import path, include
from projects.views import register  # Import register view
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('projects.urls')),  # Include API routes from the projects app
    path('api/register/', register, name='register'),  # Ensure this exists


    # path("api/projects/", include("projects.urls")),  # Your project endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/register/", include("users.urls")),  # only if you have custom register


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
