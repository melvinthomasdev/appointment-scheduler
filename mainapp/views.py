from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Teacher, Appointment, Timeslot
from .serializers import TeacherSerializer, AppointmentSerializer
from .utilities import slot_available, get_available_teachers

# Returns a list of all Teachers
def get_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return JsonResponse(serializer.data, safe=False)

# Gets a specific Teacher instance
def get_teacher(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    serializer = TeacherSerializer(teacher)
    return JsonResponse(serializer.data, safe=False)

# Home route
def home(request):
    return JsonResponse(
        {
            "message": "This is the API root",
            "Show slot availability": reverse("show_slots"),
            "Book Slot": reverse("book_slot"),
            "Get auth token": reverse("auth"),
            "List of all teachers": reverse("get_teachers")
        }
    )

# Returns Slot availability.
@api_view(['GET'])
def show_slots(request):
    if request.method == "GET":
        result = {}
        timeslots = Timeslot.objects.all()
        # Check if slot is available for all timeslots
        for timeslot in timeslots:
            result[str(timeslot)] = slot_available(timeslot)
    else:
        result["message"] = "Request is not GET!!"
    return JsonResponse(result)

# Books an appointment for the timeslot
@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def book_slot(request):
    result = {}
    if request.method == "POST":
        data = JSONParser().parse(request)
        time = data.get("timeslot")
        try:
            # Geting timeslot instance. If timeslot is invalid raises Timeslot.DoesNotExist
            timeslot = Timeslot.objects.get(time=time)
            if slot_available(timeslot): # Check slot availability
                teacher = get_available_teachers(timeslot) # Get available teacher
                # Create an appointment and save to DB
                appointment = Appointment(time=timeslot, teacher=teacher)
                appointment.save()
                result["message"] = "Success"
                return JsonResponse(result,  safe=False)
            else: # If slot not available
                result['message'] = "Timeslot not available"
        except Timeslot.DoesNotExist: # if invalid timeslot
            result["error"] = "Invalid timeslot"
            return JsonResponse(result, safe=False)
    else:
        result["message"] = "Request is not POST"
    return JsonResponse(result, safe=False)
