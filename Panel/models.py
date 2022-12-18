import time

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Setting(models.Model):
    allow_new_user = models.BooleanField(default=True, blank=False, null=False)

    def __str__(self):
        if self.allow_new_user:
            return 'در حال ثبت نام'
        else:
            return 'تکمیل ثبت نام'


class Dorm(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه')
    status = models.BooleanField(default=True, null=False, blank=False)
    code = models.CharField(max_length=64, blank=False, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)
    sex = models.BooleanField(default=False, blank=True, null=True)  # True for male, False for female

    def __str__(self):
        return f'{self.title}, {self.code}'


class Room(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه')
    status = models.BooleanField(default=True, null=False, blank=False)
    code = models.CharField(max_length=64, blank=False, null=False, unique=True)
    dorm = models.ForeignKey(to=Dorm, on_delete=models.PROTECT, blank=False, null=False, related_name='+')
    capacity = models.SmallIntegerField(blank=False, null=False, default=1)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return f'{self.title}, {self.code}, {self.dorm}'


class UserProfile(models.Model):
    USER_GRADE_OPTIONS = (
        ('کارشناسی', 'کارشناسی'),
        ('ارشد', 'ارشد'),
        ('دکترا', 'دکترا'),
        ('مدیر', 'مدیر'),
    )
    registration_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    user_instance = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=False, null=False, related_name='+')
    student_number = models.CharField(max_length=64, blank=False, null=False)
    sex = models.BooleanField(default=False, blank=True, null=True)  # True for male, False for female
    room = models.ForeignKey(to=Room, on_delete=models.PROTECT, blank=True, null=True, related_name='+')
    room_confirmed = models.BooleanField(default=False, blank=True, null=True)
    is_native_born = models.BooleanField(default=True, blank=False, null=False)
    is_paying = models.BooleanField(default=False, blank=False, null=False)
    father_name = models.CharField(max_length=32, blank=True, null=True)
    id_card_number = models.SmallIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    is_early_bird = models.BooleanField(default=False, blank=False, null=False)
    grade = models.CharField(max_length=16, blank=False, null=False, default='کارشناسی', choices=USER_GRADE_OPTIONS)
    requested_roommate = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=True, null=True, default=None,
                                           related_name='+')
    is_noisy = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f'{self.student_number}'
