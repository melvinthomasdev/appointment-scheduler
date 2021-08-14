from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
time_choices = (
    ("10:00", "10:00"),
    ("10:30", "10:30"),
    ("11:00", "11:00"),
    ("11:30", "11:30"),
    ("12:00", "12:00"),
    ("12:30", "12:30"),
    ("13:00", "13:00"),
    ("13:30", "13:30"),
    ("14:00", "14:00"),
    ("14:30", "14:30"),
    ("15:00", "15:00"),
    ("15:30", "15:30"),
    ("16:00", "16:00"),
    ("16:30", "16:30")
)


class Teacher(models.Model):
    name = models.CharField(max_length=35, null=False)
    # available_slots = all_slots
    
    def __str__(self):
        return self.name

class Timeslot(models.Model):
    time = models.CharField(max_length=5, null=False, choices=time_choices, unique=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.time

class Appointment(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='teachers', on_delete=models.CASCADE)
    # time = models.CharField(max_length=5, null=False, choices=time_choices, unique=True)

    time = models.ForeignKey('Timeslot', related_name='appointment', on_delete=models.CASCADE)
    # student = models.ForeignKey(User, related_name='appointment', on_delete=models.CASCADE)    

    def __str__(self):
        # res = ""
        # for i in self.teachers.all():
        #     res+=i.name+ " "
        # return res
        return self.teacher.name
    
    # def number_of_teachers(self):
    #     return len(self.teachers.all())

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)