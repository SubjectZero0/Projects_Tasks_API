from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

# --------------------------------------------------------------

class CustomUserManager(BaseUserManager):
    """
    Custom manager for handling user creation.
    """

    def create_user(self, email, name, password=None, **extra_field):
        """
        Method to create a regular user
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=email, name=name, **extra_field)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, name, password):
        """
        Method to create a superuser
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user

# --------------------------------------------------------------


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as a credential.
    """
    email = models.EmailField(max_length=30, unique=True, default='n@n.n')

    name = models.CharField(max_length=30, null=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

# --------------------------------------------------------------


class Projects(models.Model):
    """
    Model for Oganization's Projects
    """
    project_id = models.BigAutoField(primary_key=True)

    project_title = models.CharField(max_length=100, unique=True)

    project_descr = models.TextField(max_length=300, blank=True, null=True)

    project_prog_percent = models.IntegerField(default=0)

    project_finish_date = models.DateField(blank=True, null=True)

    project_owner = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.project_title


class Tasks(models.Model):
    """
    Model for Projects' Tasks
    """
    task_title = models.CharField(max_length=100)

    task_descr = models.TextField(max_length=300, blank=True, null=True)

    task_prog_percent = models.IntegerField(default=0)

    task_finish_date = models.DateField(blank=True, null=True)

    task_tags = models.ManyToManyField('Tags', blank=True)

    task_owner = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE)

    parent_project = models.ForeignKey(
        'Projects', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.task_title


class Tags(models.Model):
    """
    Model for Tasks' Tags.
    """
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name

# --------------------------------------------------------------------
