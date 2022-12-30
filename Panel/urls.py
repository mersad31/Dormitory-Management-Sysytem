from .views import home, login, register, room_management, student_management, dorm_management, logout_view
from django.urls import path

urlpatterns = [
    path('', home, name='HomePage'),
    path('login', login, name='Login'),
    path('logout', logout_view, name='Logout'),
    path('register', register, name='Register'),
    path('room-management', room_management, name='Room'),
    path('student-management', student_management, name='Student'),
    path('dorm-management', dorm_management, name='Dorm'),
]
