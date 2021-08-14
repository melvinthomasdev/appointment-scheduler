from .models import Teacher, Appointment, Timeslot

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

def get_available_teachers(slot):
    available_teachers = []
    timeslot = Timeslot.objects.get(time=slot)
    teachers = Teacher.objects.all()
    for teacher in teachers:
        appointments = Appointment.objects.filter(teachers__in=[teacher], time=timeslot)
        if len(appointments)==0:
            available_teachers.append(teacher)
            if len(available_teachers)>1:
                return available_teachers