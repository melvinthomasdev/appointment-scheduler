from django.contrib import admin

from .models import Teacher, Appointment, Timeslot
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Timeslot)

class AppointmentAdmin(admin.ModelAdmin):
    # list_display = ["__str__", "time", "number_of_teachers"]
    list_display = ["__str__", "time"]


admin.site.register(Appointment, AppointmentAdmin)
