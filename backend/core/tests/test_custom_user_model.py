"""
Tests for CustomUser model and Manager.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

# ---------------------------------------------------------------------


class CustomUserModelTests(TestCase):
    """
    Tests for the CustomUser Model
    """

    def test_create_user(self):
        """
        Test for creating a regular user
        """
        user_cred = {
            'email': 'test@email.com',
            'name': 'test_name',
            'password': 'password'
        }

        user = get_user_model().objects.create_user(**user_cred)

        self.assertEqual(user.email, user_cred['email'])
        self.assertEqual(user.name, user_cred['name'])
        self.assertTrue(user.check_password(user_cred['password']))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Test for creating a superuser
        """
        superuser_cred = {
            'email': 'test@email.com',
            'name': 'test_name',
            'password': 'password'
        }

        user = get_user_model().objects.create_superuser(**superuser_cred)

        self.assertEqual(user.email, superuser_cred['email'])
        self.assertEqual(user.name, superuser_cred['name'])
        self.assertTrue(user.check_password(superuser_cred['password']))
        self.assertTrue(user.is_superuser)
