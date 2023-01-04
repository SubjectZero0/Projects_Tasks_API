from django.contrib import admin
from .models import CustomUser, Projects, Tags, Tasks

# Register your models here.


admin.site.register(CustomUser)

admin.site.register(Projects)

admin.site.register(Tags)

admin.site.register(Tasks)
