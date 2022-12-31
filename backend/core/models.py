from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

#--------------------------------------------------------------
class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation
    """
    def create_user(self, username, password=None):
        """
        Method to create a regular user
        """
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(self.strip(username))
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self,username,password):
        """
        Method to create a superuser
        """
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True

        return user

#--------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with only username
    """
    username = models.CharField(max_length=30, unique=True)

    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username