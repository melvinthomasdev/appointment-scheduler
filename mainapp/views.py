from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Teacher, Appointment, Timeslot
from .serializers import TeacherSerializer, AppointmentSerializer
from .utilities import slot_available, get_available_teachers
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
    if request.method == "GET":
        result = {}
        timeslots = Timeslot.objects.all()
        for timeslot in timeslots:
            result[str(timeslot)] = slot_available(timeslot)
    else:
        result["message"] = "Request is not GET!!"
    return JsonResponse(result)

@csrf_exempt
def book_slot(request):
    result = {}
    if request.method == "POST":
        data = JSONParser().parse(request)
        time = data.get("timeslot")
        try:
            timeslot = Timeslot.objects.get(time=time)
            if slot_available(timeslot):
                teacher = get_available_teachers(timeslot)
                appointment = Appointment(time=timeslot, teacher=teacher)
                appointment.save()
                # for teacher in teachers:
                #     appointment.teachers.add(teacher)
                # serializer = AppointmentSerializer(appointment)
                result["message"] = "Success"
                return JsonResponse(result,  safe=False)
            else:
                result['message'] = "Timeslot not available"
        except Timeslot.DoesNotExist:
            result["error"] = "Invalid timeslot"
            return JsonResponse(result, safe=False)
    else:
        result["message"] = "Request is not POST"
    return JsonResponse(result, safe=False)
