from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required 
from .models import Appointment, Pet, Vaccines
from .forms import AppointmentForm, Petform, RegisterForm
import logging


""" Vistas de MASCOTAS (PETS)"""

# READ MÚLTIPLE PETS
@login_required
def view_pets(request):
    if request.user.is_staff:
        all_pets = Pet.objects.all()
        logging.info(f"Mostrando todas las mascotas del centro por el usuario {request.user}.")
    else:
        all_pets = Pet.objects.filter(user=request.user)
        logging.info(f"Mostrando todas las mascotas del usuario {request.user}.")
    return render(request, 'mascotas.html', {'mascotas': all_pets})

# READ INDIVIDUAL PET
@login_required
def view_detail(request, id_pet):
    pet_select = get_object_or_404(Pet, id=id_pet)
    logging.info(f"Mostrando detalles de la mascota {pet_select.name}.")
    return render(request, "detalle_mascota.html", {"mascota": pet_select})


# CREATE PET
@login_required
def view_create_pet(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de creación de mascotas sin permisos.")
        return redirect("mascotas") 

    if request.method == "POST":
        form = Petform(request.POST)
        logging.info(f"El usuario {request.user} está intentando crear una nueva mascota.")
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            logging.info(f"La mascota {pet.name} fue asignada a {pet.user} exitosamente por {request.user}.")
            return redirect("mascotas")
    else:
        form = Petform()
        logging.info(f"El usuario {request.user} accedió a la vista de creación de mascotas.")

    return render(request, "formulario.html", {
        "form": form,
        "titulo": "Crear mascota"
    })

# UPDATE PET
@login_required
def view_edit_pet(request, id_pet):
    old_pet = get_object_or_404(Pet, id=id_pet)

    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de edición de mascotas sin permisos.")   
        return redirect("mascotas") 
    
    if request.method == "POST":
        form = Petform(request.POST, instance=old_pet)
        if form.is_valid():
            form.save()
            logging.info(f"La mascota {old_pet.name} fue actualizada exitosamente por el usuario {request.user}.")
            return redirect("detalle mascota", id_pet=old_pet.id)
    else:
        form = Petform(instance=old_pet)
    return render(request, "formulario.html", {"form": form, "titulo": "Editar mascota"})


# DELETE PET
@login_required
def view_del_pet(request, id_pet):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó eliminar una mascota sin permisos.")
        return redirect("mascotas")

    if request.method == "POST":
        pet = get_object_or_404(Pet, id=id_pet)
        pet_name = pet.name
        pet.delete()
        logging.info(f"La mascota {pet_name} fue eliminada exitosamente por el usuario {request.user}.")
    
    return redirect("mascotas")


""" Vistas de CITAS (APPOINTMENTS)"""

# READ CITAS
@login_required
def view_appointments(request):
    if request.user.is_staff:
        all_appointments = Appointment.objects.all()
        logging.info(f"Mostrando todas las citas médicas por el usuario {request.user}.")
    else:
        all_appointments = Appointment.objects.filter(user=request.user)
        logging.info(f"Mostrando citas médicas del usuario {request.user}.")
    return render(request, "citas.html", {"citas": all_appointments})

# CREATE CITAS
@login_required 
def view_create_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            logging.info(f"La cita médica fue creada exitosamente por el usuario {request.user}.")
            return redirect("citas")
    else:
        form = AppointmentForm()
        logging.info(f"El usuario {request.user} accedió a la vista de creación de citas médicas.")

    return render(request, "añadir_cita.html", {"form": form, "titulo": "Crear cita"})

# DELETE CITAS
@login_required 
def view_del_appointment(request, id_appointment):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de eliminación de citas médicas sin permisos.")
        return redirect("mascotas") 
    
    appointment = get_object_or_404(Appointment, id=id_appointment)
    if request.method == "POST":
        appointment.delete()
        logging.info(f"La cita médica con ID {id_appointment} fue eliminada exitosamente por el usuario {request.user}.")
        return redirect("citas")
    return render(request, "confirmar_borrado.html", {"Cita": appointment}) 


""" Vistas de VACUNAS """

# READ VACUNAS
@login_required
def view_vaccines(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de vacunas sin permisos.")
        return redirect("mascotas") 
    
    all_vaccines = Vaccines.objects.all()
    logging.info(f"Mostrando todas las vacunas por el usuario {request.user}.")
    return render(request, "vacunas.html", {"vacunas": all_vaccines})

# CREATE VACUNAS
@login_required
def view_create_vaccine(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de creación de vacunas sin permisos.")
        return redirect("mascotas") 
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        vaccine = Vaccines(name=name, description=description)
        vaccine.save()
        logging.info(f"La vacuna {vaccine.name} fue creada exitosamente por el usuario {request.user}.")
        return redirect("vacunas")
    else:
        logging.info(f"El usuario {request.user} accedió a la vista de creación de vacunas.")
    return render(request, "añadir_vacuna.html", {"titulo": "Crear vacuna"})

# DELETE VACUNAS
@login_required
def view_del_vaccine(request, id_vaccine):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de eliminación de vacunas sin permisos.")
        return redirect("mascotas") 
    
    vaccine = get_object_or_404(Vaccines, id=id_vaccine)
    if request.method == "POST":
        vaccine.delete()
        logging.info(f"La vacuna {vaccine.name} fue eliminada exitosamente por el usuario {request.user}.")
        return redirect("vacunas")
    return render(request, "confirmar_borrado.html", {"Vacuna": vaccine})


""" Vistas de REGISTRO USUARIO """

# REGISTRO USER
def view_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            logging.info(f"El usuario {user.username} se registró exitosamente.")   
            return redirect("mascotas")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})