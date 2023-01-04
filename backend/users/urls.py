from django.urls import path
from .views import ObtainTokenView
# -----------------------------------------------------------------

app_name = 'users'

# -----------------------------------------------------------------

urlpatterns = [
    path('login/', ObtainTokenView.as_view(), name='login')
]
