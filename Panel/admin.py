from django.contrib import admin
from .models import Dorm, Room, Setting, UserProfile

# Register your models here.
admin.site.register(Dorm)
admin.site.register(Room)
admin.site.register(Setting)
admin.site.register(UserProfile)
