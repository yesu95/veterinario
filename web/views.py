from django.shortcuts import get_object_or_404, render, redirect
from .models import Appointment, Pet, Vaccines
from .forms import Petform


# READ MÚLTIPLE
def view_pets(request):
    # ORM: Toma todas las mascotas de la base de datos
    all_pets = Pet.objects.all()
    # Enviamos en minúscula y plural por convención
    return render(request, "mascotas.html", {"mascotas": all_pets})


# READ INDIVIDUAL
def view_detail(request, id_pet):
    # Devuelve el objeto o un error 404
    pet_select = get_object_or_404(Pet, id=id_pet)
    return render(request, "detalle_mascota.html", {"mascota": pet_select})


# CREATE
def view_create_pet(request):
    if request.method == "POST":
        form = Petform(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('mascotas')
    else:
        form = Petform() # Formulario en blanco esperando
        
    return render(request, 'formulario.html', {'form': form})


# UPDATE
def view_edit_pet(request, id_pet):
    old_pet = get_object_or_404(Pet, id=id_pet)
    if request.method == "POST":
        # Metemos los datos nuevos (POST), pero avisando de que sobreescriban a (instance=old_pet)
        form = Petform(request.POST, instance=old_pet)
        if form.is_valid():
            form.save()
            return redirect('detalle', id_pet=old_pet.id)
    else:
        form = Petform(instance=old_pet) # Formulario YA relleno
    return render(request, 'formulario.html', {'form': form})


# DELETE 
def view_del_pet(request, id_pet):
    pet = get_object_or_404(Pet, id=id_pet)
    if request.method == "POST":
        pet.delete()
        return redirect('catalogo')
    return render(request, 'confirmar_borrado.html', {'Mascota': pet})