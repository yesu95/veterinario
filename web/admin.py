from django.contrib import admin
from .models import User, Pet, Vaccines, Appointment

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Vaccines)
admin.site.register(Appointment)