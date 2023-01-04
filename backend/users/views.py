from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .serializers import LoginSerializer
# --------------------------------------------------------------------

# Create your views here.


class ObtainTokenView(ObtainAuthToken):
    """
    Authentication/Token view
    """

    serializer_class = LoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
