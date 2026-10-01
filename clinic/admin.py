
from django.contrib import admin
from .models import (
    Appointment,
    Doctor,
    Medicine,
    VirtualAssistance,
    EmergencyRequest,
)

admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(Medicine)
admin.site.register(VirtualAssistance)
admin.site.register(EmergencyRequest)