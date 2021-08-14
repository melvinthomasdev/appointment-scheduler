from .models import Teacher, Appointment, Timeslot

# Checks if 2 teachers are available for a timeslot
def slot_available(slot):
    teachers = Teacher.objects.all()
    timeslot = Timeslot.objects.get(time=slot)
    number_of_teachers = 0
    for teacher in teachers:
        # Check for an appointment for a teacher for a slot
        appointments = Appointment.objects.filter(teacher=teacher, time=timeslot)
        if len(appointments)==0:
            # If a teacher doesn't have an appointment for the slot, that teacher is available.
            number_of_teachers+=1
            if number_of_teachers>1:
                return True
    return False

# Returns a Teacher object that is available
def get_available_teachers(slot):
    timeslot = Timeslot.objects.get(time=slot)
    teachers = Teacher.objects.all()
    for teacher in teachers:
        # Checks if a Teacher has an appointment for the specified timeslot
        appointments = Appointment.objects.filter(teacher=teacher, time=timeslot)
        if len(appointments)==0:
            return teacher