from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Dorm(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه')
    status = models.BooleanField(default=True, null=False, blank=False)
    code = models.CharField(max_length=64, blank=False, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return f'{self.title}, {self.code}'


class Room(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه')
    status = models.BooleanField(default=True, null=False, blank=False)
    code = models.CharField(max_length=64, blank=False, null=False, unique=True)
    dorm = models.ForeignKey(to=Dorm, on_delete=models.PROTECT, blank=False, null=False)
    capacity = models.SmallIntegerField(blank=False, null=False, default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return f'{self.title}, {self.code}, {self.dorm}'


class UserProfile(models.Model):
    user_instance = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=False, null=False)
    user_code = models.CharField(max_length=64, blank=False, null=False)
    room = models.ForeignKey(to=Room, on_delete=models.PROTECT, blank=True, null=True)
