from django.contrib import admin
from .models import *

admin.site.register(Patient)
admin.site.register(Insurance)
admin.site.register(Allergies)
admin.site.register(Vitals)
admin.site.register(Diagnosis)
admin.site.register(Phys_Orders)
admin.site.register(Prescription)
admin.site.register(Vaccines)
admin.site.register(Appointment)
admin.site.register(Bills)



