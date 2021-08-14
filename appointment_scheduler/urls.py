from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from mainapp.views import get_teachers, get_teacher, show_slots, book_slot, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('teachers/', get_teachers, name="get_teachers"),
    path('teacher/<int:pk>', get_teacher, name="get_teacher"),
    path('api/teacher/show-availability', show_slots, name="show_slots"),
    path('api/teacher/book', book_slot, name="book_slot"),
    path('api/auth', obtain_auth_token, name="auth"),
]
