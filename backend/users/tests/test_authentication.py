from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

# --------------------------------------------------------------------

LOGIN_URL = reverse('users:login')

# --------------------------------------------------------------------


class TokenAuthTests(APITestCase):
    """
    Tests for authenticating users with the Token Authentication system.
    """

    def test_token_generation(self):
        """
        Tests if a token is generated upon authentication request
        """
        superuser_cred = {
            'email': 'test@email.com',
            'name': 'test_name',
            'password': 'password'
        }

        superuser = get_user_model().objects.create_superuser(**superuser_cred)

        payload = {
            'email': superuser_cred['email'],
            'password': superuser_cred['password']
        }

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
