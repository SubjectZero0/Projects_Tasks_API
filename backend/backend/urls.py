"""
backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from projects.views import ProjectAPIViewSet, TaskAPIViewSet
# --------------------------------------------------------------
router = routers.DefaultRouter()
router.register('projects', ProjectAPIViewSet, basename='projects')
router.register('tasks', TaskAPIViewSet, basename='tasks')
# ---------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('dataverse_api/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
]
