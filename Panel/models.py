import time

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Setting(models.Model):
    allow_new_user = models.BooleanField(default=True, blank=False, null=False, verbose_name='وضعیت ثبت نام')

    def __str__(self):
        if self.allow_new_user:
            return 'در حال ثبت نام'
        else:
            return 'تکمیل ثبت نام'

    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"


class Dorm(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه', verbose_name='عنوان')
    status = models.BooleanField(default=True, null=False, blank=False, verbose_name='وضعیت')
    code = models.CharField(max_length=64, blank=False, null=False, unique=True, verbose_name='کد')
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False,
                                        verbose_name='زمان ایجاد')
    sex = models.BooleanField(default=False, blank=True, null=True,
                              verbose_name='جنسیت')  # True for male, False for female

    def __str__(self):
        return f'{self.title}, {self.code}'

    class Meta:
        verbose_name = "خوابگاه"
        verbose_name_plural = "خوابگاه ها"


class Room(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False, default='خوابگاه', verbose_name='عنوان')
    status = models.BooleanField(default=True, null=False, blank=False, verbose_name='وضعیت')
    code = models.CharField(max_length=64, blank=False, null=False, unique=True, verbose_name='کد')
    dorm = models.ForeignKey(to=Dorm, on_delete=models.PROTECT, blank=False, null=False, related_name='+',
                             verbose_name='خوابگاه مورد نظر')
    capacity = models.SmallIntegerField(blank=False, null=False, default=1, verbose_name='ظرفیت')
    created_date = models.DateTimeField(auto_now_add=True, blank=False, null=False, editable=False,
                                        verbose_name='زمان ایجاد')

    def __str__(self):
        return f'{self.title}, {self.code}, {self.dorm}'

    class Meta:
        verbose_name = "اتاق"
        verbose_name_plural = "اتاق ها"


class UserProfile(models.Model):
    USER_GRADE_OPTIONS = (
        ('کارشناسی', 'کارشناسی'),
        ('ارشد', 'ارشد'),
        ('دکترا', 'دکترا'),
        ('مدیر', 'مدیر'),
    )
    registration_date = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name='زمان ثبت نام')
    user_instance = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=False, null=False, related_name='+',
                                      verbose_name='کاربر')
    student_number = models.CharField(max_length=64, blank=False, null=False, verbose_name='شماره دانشجویی')
    sex = models.BooleanField(default=False, blank=True, null=True,
                              verbose_name='جنسیت')  # True for male, False for female
    room = models.ForeignKey(to=Room, on_delete=models.PROTECT, blank=True, null=True, related_name='+',
                             verbose_name='اتاق مورد نظر')
    room_confirmed = models.BooleanField(default=False, blank=True, null=True, verbose_name='وضعیت تاییدیه اتاق')
    is_native_born = models.BooleanField(default=True, blank=False, null=False, verbose_name='دانشجو بومی هستم')
    is_paying = models.BooleanField(default=False, blank=False, null=False, verbose_name='دانشجو شبانه هستم')
    father_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='نام پدر')
    id_card_number = models.SmallIntegerField(blank=True, null=True, verbose_name='کد ملی')
    phone_number = models.CharField(max_length=16, blank=True, null=True, verbose_name='شماره تماس')
    is_early_bird = models.BooleanField(default=False, blank=False, null=False, verbose_name='سحر خیز بودن')
    grade = models.CharField(max_length=16, blank=False, null=False, default='کارشناسی', choices=USER_GRADE_OPTIONS,
                             verbose_name='مقطع تحصیلی')
    requested_roommate = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=True, null=True, default=None,
                                           related_name='+', verbose_name='هم اتاقی مورد نظر')
    is_noisy = models.BooleanField(default=False, blank=False, null=False, verbose_name='حساس به سر صدا')

    def __str__(self):
        return f'{self.student_number}'

    class Meta:
        verbose_name = "پروفایل گاربری"
        verbose_name_plural = "پروفایل های گاربری"
