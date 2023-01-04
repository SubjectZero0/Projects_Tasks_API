from rest_framework.serializers import Serializer, ValidationError
from rest_framework import serializers

from django.contrib.auth import authenticate

# --------------------------------------------------------------------


class LoginSerializer(Serializer):
    """
    Serializer for logging in. Used to obtain a token
    """
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        auth_user = authenticate(username=email, password=password)

        if auth_user is not None:
            data['user'] = auth_user
            return data
        else:
            raise ValidationError(
                'Please enter valid credentials', code='authorization')
