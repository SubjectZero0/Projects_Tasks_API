"""backend URL Configuration
"""
from django.contrib import admin
from django.urls import path,include


from rest_framework import routers


from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
#--------------------------------------------------------------
router = routers.DefaultRouter()

#---------------------------------------------------------------
urlpatterns = [
    path('admin/', admin.site.urls),


    path('api/schema/', SpectacularAPIView.as_view(), name = 'api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
]
