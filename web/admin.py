from django.contrib import admin
from .models import Pet, Vaccines, Appointment

admin.site.register(Pet)
admin.site.register(Vaccines)
admin.site.register(Appointment)