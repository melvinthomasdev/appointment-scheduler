from .models import Teacher, Appointment, Timeslot
# from .models import all_slots

def slot_available(slot):
    teachers = Teacher.objects.all()
    timeslot = Timeslot.objects.get(time=slot)
    number_of_teachers = 0
    for teacher in teachers:
        appointments = Appointment.objects.filter(teachers__in=[teacher], time=timeslot)
        if len(appointments)==0:
            number_of_teachers+=1
            if number_of_teachers>1:
                return True
    return False