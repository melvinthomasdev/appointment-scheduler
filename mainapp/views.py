from django.shortcuts import render
from django.http import JsonResponse

from .models import Teacher, Appointment, Timeslot
from .serializers import TeacherSerializer, AppointmentSerializer
from .utilities import slot_available
# Create your views here.

def get_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return JsonResponse(serializer.data, safe=False)

def get_teacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    serializer = TeacherSerializer(teacher)
    return JsonResponse(serializer.data, safe=False)



def show_slots(request):
    result = {}
    timeslots = Timeslot.objects.all()
    for timeslot in timeslots:
        result[str(timeslot)] = slot_available(timeslot)
    return JsonResponse(result)


