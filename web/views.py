
from django.shortcuts import render, get_object_or_404
from .models import Pet, Vaccines, Appointment

# EL LISTADO (READ múltiple del CRUD)
def view_pet(request):
    # ORM: Toma todas las mascotas de la base de datos
    all_pets = Pet.objects.all()
    # 'render' une el diccionario de ingredientes Python con el diseño HTML base.
    return render(request, "mascotas.html", {"Mascota": all_pets})

# EL DETALLE (READ individual del CRUD)
def vista_detalle(request, id_pet):
    # Si piden el id 99 pero no existe, levanta de golpe una pantalla 404 Not Found automáticamente
    pet_select = get_object_or_404(Pet, id=id_pet)
    return render(request,"2detalle_mascota.html", {"Macota": pet_select})