from django.shortcuts import get_object_or_404, render
from .models import Appointment, Pet, Vaccines

# EL LISTADO (READ múltiple del CRUD)
def view_pet(request):
    # ORM: Toma todas las mascotas de la base de datos
    all_pets = Pet.objects.all()
    # Enviamos en minúscula y plural por convención
    return render(request, "mascotas.html", {"mascotas": all_pets})

# EL DETALLE (READ individual del CRUD)
def vista_detalle(request, id_pet):
    # Devuelve el objeto o un error 404
    pet_select = get_object_or_404(Pet, id=id_pet)
    # Corregido: "mascota" en lugar de "Macota"
    return render(request, "2detalle_mascota.html", {"mascota": pet_select})