from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required   
from .models import Appointment, Pet, Vaccines
from .forms import Petform


""" Vistas de MASCOTAS (PETS)"""

# READ MÚLTIPLE PETS
@login_required
def view_pets(request):
    if request.user.is_staff:
        all_pets = Pet.objects.all()
    else:
        all_pets = Pet.objects.filter(user=request.user)
    return render(request, 'mascotas.html', {'mascotas': all_pets})

# READ INDIVIDUAL PET
@login_required
def view_detail(request, id_pet):
    pet_select = get_object_or_404(Pet, id=id_pet)
    return render(request, "detalle_mascota.html", {"mascota": pet_select})


# CREATE PET
""" Si NO es staff, me devuelve a mascotas, SI ES me pinta /añadir """
@login_required
def view_create_pet(request):
    if not request.user.is_staff:
        return redirect("mascotas") 
    
    if request.method == "POST":
        form = Petform(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            return redirect("mascotas")
    else:
        form = Petform() # Formulario en blanco esperando
        
    return render(request, "formulario.html", {"form": form})


# UPDATE PET
@login_required
def view_edit_pet(request, id_pet):
    old_pet = get_object_or_404(Pet, id=id_pet)

    if not request.user.is_staff:
        return redirect("mascotas") 
    
    if request.user.is_staff and request.method == "POST":
        # Metemos los datos nuevos (POST), pero avisando de que sobreescriban a (instance=old_pet)
        form = Petform(request.POST, instance=old_pet)
        if form.is_valid():
            form.save()
            return redirect("detalle", id_pet=old_pet.id)
    else:
        form = Petform(instance=old_pet) # Formulario YA relleno
    return render(request, "formulario.html", {"form": form})


# DELETE PET
@login_required
def view_del_pet(request, id_pet):
    if not request.user.is_staff:
        return redirect("mascotas") 
    
    if request.user.is_staff:
        pet = get_object_or_404(Pet, id=id_pet)
        if request.method == "POST":
            pet.delete()
            return redirect("mascotas")
        return render(request, "confirmar_borrado.html", {"Mascota": pet})

""" Vistas de CITAS (APPOINTMENTS)"""

# READ CITAS
@login_required
def view_appointments(request):
    if request.user.is_staff:
        all_appointments = Appointment.objects.all()
        return render(
    request, "citas.html", {"citas": all_appointments})
    else:
        all_appointments = Appointment.objects.filter(user=request.user)
        return render(
            request, "citas.html", {"citas": all_appointments})


""" Vistas de VACUNAS """

# READ VACUNAS
@login_required
def view_vaccines(request):
    if not request.user.is_staff:
        return redirect("mascotas") 
    if request.user.is_staff:
        all_vaccines = Vaccines.objects.all()
        return render(
            request, "vacunas.html", {"vacunas": all_vaccines}
    )


# ERROR 404
def view_404(request, exception=None):
    return redirect('/') 
