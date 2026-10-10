from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required 
from .models import Appointment, Pet, Vaccines
from .forms import AppointmentForm, Petform, RegisterForm, VaccineForm
from .exceptions import VetError, PetError, AppointmentError, VaccineError
from django.db import DatabaseError
import logging


""" Vistas de MASCOTAS (PETS)"""

# READ MÚLTIPLE PETS
""" SI es staff muestra todas las mascotas del centro SINO muestra solo las mascotas del usuario logueado"""
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
""" SI NO es staff y mascota NO pertenece al usuario logueado, redirige a vista mascotas. SIGUE hasta muestra detalle de la mascota"""
@login_required
def view_detail(request, id_pet):
    pet_select = get_object_or_404(Pet, id=id_pet)

    # No permitir que el usuario vea mascotas que no son suyas a menos que sean staff
    if not request.user.is_staff and pet_select.user != request.user:
        logging.warning(f"El usuario '{request.user}' intentó ver la mascota '{pet_select.name}' que no es suya.")
        return redirect("mascotas")

    logging.info(f"Mostrando detalles de la mascota '{pet_select.name}'.")
    return render(request, "detalle_mascota.html", {"mascota": pet_select})

# CREATE PET
"""" 
    SI NO es staff, redirige a vista mascotas. SIGUE hasta crear mascota y asignarla a un usuario. 
    SI el usuario tiene una mascota con mismo nombre, excepción PetError y MUESTRA mensaje de error.
"""
@login_required
def view_create_pet(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario {request.user} intentó acceder a la vista de creación de mascotas sin permisos.")
        return redirect("mascotas") 

    if request.method == "POST":
        form = Petform(request.POST)
        logging.info(f"El usuario {request.user} está intentando crear una nueva mascota.")
        if form.is_valid():
            try:
                pet = form.save(commit=False)
                owner = form.cleaned_data["user"]
                if Pet.objects.filter(user=owner, name=pet.name).exists():
                    raise PetError("Ese propietario ya tiene una mascota con ese nombre.")
                pet.user = owner
                pet.save()
                logging.info(f"La mascota '{pet.name}' fue asignada a '{pet.user}' exitosamente por '{request.user}'.")
                return redirect("mascotas")

            except PetError as e:
                logging.warning(f"Mascota duplicada al intentar crearla: '{e}'")
                form.add_error("name", str(e))

            except DatabaseError as e:
                logging.error(f"Error de base de datos al guardar la mascota: '{e}'")
                form.add_error(None, "No se pudo guardar la mascota. Inténtalo de nuevo.")
    else:
        form = Petform()
        logging.info(f"El usuario '{request.user}' accedió a la vista de creación de mascotas.")

    return render(request, "formulario.html", {
        "form": form,
        "titulo": "Crear mascota"
    })


# UPDATE PET
""" SI NO es staff, redirige a vista mascotas. SIGUE hasta editar mascota y asignarla a un usuario."""
@login_required
def view_edit_pet(request, id_pet):
    old_pet = get_object_or_404(Pet, id=id_pet)

    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó acceder a la vista de edición de mascotas sin permisos.")   
        return redirect("mascotas") 
    
    if request.method == "POST":
        form = Petform(request.POST, instance=old_pet)
        if form.is_valid():
            form.save()
            logging.info(f"La mascota '{old_pet.name}' fue actualizada exitosamente por el usuario '{request.user}'.")
            return redirect("detalle mascota", id_pet=old_pet.id)
    else:
        form = Petform(instance=old_pet)
    return render(request, "formulario.html", {"form": form, "titulo": "Editar mascota"})


# DELETE PET
""" SI NO es staff, redirige a vista mascotas. SIGUE hasta eliminar mascota."""
@login_required
def view_del_pet(request, id_pet):
    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó eliminar una mascota sin permisos.")
        return redirect("mascotas")

    if request.method == "POST":
        pet = get_object_or_404(Pet, id=id_pet)
        pet_name = pet.name
        pet.delete()
        logging.info(f"La mascota '{pet_name}' fue eliminada exitosamente por el usuario '{request.user}'.")
    
    return redirect("mascotas")


""" Vistas de CITAS (APPOINTMENTS)"""

# READ CITAS
""" SI es staff muestra todas las citas médicas del centro SINO muestra solo las citas médicas del usuario logueado."""
@login_required
def view_appointments(request):
    if request.user.is_staff:
        all_appointments = Appointment.objects.all()
        logging.info(f"Mostrando todas las citas médicas por el usuario '{request.user}'.")
    else:
        all_appointments = Appointment.objects.filter(user=request.user)
        logging.info(f"Mostrando citas médicas del usuario '{request.user}'.")
    return render(request, "citas.html", {"citas": all_appointments})


# CREATE CITAS
"""" SI NO es staff, redirige a vista mascotas. SI SIGUE crea cita médica y la asigna a un usuario."""
@login_required 
def view_create_appointment(request):
    form = AppointmentForm(request.POST or None)

    # Si el user es staff, borra el desplegable de usuarios.
    if not request.user.is_staff:
        del form.fields["user"]

    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        if not request.user.is_staff:
            appointment.user = request.user
        appointment.save()
        logging.info(f"La cita médica fue creada exitosamente por el usuario '{request.user}'.")
        return redirect("citas")

    return render(request, "añadir_cita.html", {"form": form, "titulo": "Crear cita"})

# DELETE CITAS
""" SI NO es staff, redirige a vista mascotas. SI SIGUE se elimina cita médica."""
@login_required 
def view_del_appointment(request, id_appointment):
    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó acceder a la vista de eliminación de citas médicas sin permisos.")
        return redirect("mascotas") 
    
    appointment = get_object_or_404(Appointment, id=id_appointment)
    if request.method == "POST":
        appointment.delete()
        logging.info(f"La cita médica con ID '{id_appointment}' fue eliminada exitosamente por el usuario '{request.user}'.")
        return redirect("citas")
    return render(request, "citas.html", {"Cita": appointment}) 


""" Vistas de VACUNAS """

# READ VACUNAS
""" SI NO es staff, redirige a vista mascotas. SI SIGUE muestra todas las vacunas."""
@login_required
def view_vaccines(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó acceder a la vista de vacunas sin permisos.")
        return redirect("mascotas") 
    
    all_vaccines = Vaccines.objects.all()
    logging.info(f"Mostrando todas las vacunas por el usuario '{request.user}'.")
    return render(request, "vacunas.html", {"vacunas": all_vaccines})


# CREATE VACUNAS
""" SI NO es staff, redirige a vista mascotas. SI SIGUE crea vacuna y la asigna a un usuario."""
@login_required
def view_create_vaccine(request):
    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó acceder a la vista de creación de vacunas sin permisos.")
        return redirect("mascotas")

    form = VaccineForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        vaccine = form.save()
        logging.info(f"La vacuna '{vaccine.name_vaccine}' fue asignada a '{vaccine.pet}' por el usuario '{request.user}'.")
        return redirect("vacunas")

    return render(request, "añadir_vacuna.html", {"form": form, "titulo": "Crear vacuna"})

# DELETE VACUNAS
""" SI NO es staff, redirige a vista mascotas. SI SIGUE se elimina vacuna."""
@login_required
def view_del_vaccine(request, id_vaccine):
    if not request.user.is_staff:
        logging.warning(f"El usuario '{request.user}' intentó acceder a la vista de eliminación de vacunas sin permisos.")
        return redirect("mascotas") 
    
    vaccine = get_object_or_404(Vaccines, id=id_vaccine)
    if request.method == "POST":
        vaccine.delete()
        logging.info(f"La vacuna '{vaccine.name_vaccine}' fue eliminada exitosamente por el usuario '{request.user}'.")
        return redirect("vacunas")
    return render(request, "vacunas.html", {"Vacuna": vaccine})


""" Vistas de REGISTRO USUARIO """

# REGISTRO USER
""" SI el usuario ya está logueado, redirige a vista mascotas. SI SIGUE crea usuario y lo asigna a un usuario."""
def view_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                logging.info(f"El usuario '{user.username}' se registró exitosamente.")
                return redirect("mascotas")
            except DatabaseError as e:
                logging.error(f"Error al registrar el usuario: {e}")
                form.add_error(None, "No se pudo completar el registro. Inténtalo de nuevo.")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})