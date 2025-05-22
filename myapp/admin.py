from django.contrib import admin
from .models import DosageForm, DrugClass, Business, Patient, Appointment, DosageTime, Manufacturer, Drug, Generic, Indication, Prescription

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(DosageTime)
admin.site.register(Drug)
admin.site.register(Generic)
admin.site.register(Prescription)
admin.site.register(DosageForm)
admin.site.register(DrugClass)
admin.site.register(Indication)
admin.site.register(Manufacturer)
admin.site.register(Business)