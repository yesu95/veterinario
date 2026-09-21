from django.db import models
import datetime

# Modelo de datos para la tabla de USUARIOS 
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"Usario: {self.name} - Email: {self.email}"

# Modelo de datos para la tabla de MASCOTAS 
class Pet(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE) # FK del usuario
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=80)
    breed = models.CharField(max_length=80)
    birth_date = models.DateField(auto_now_add=True)

    """ 
    Propiedad para calcular la edad de la mascota en años.
    años_vivos es igual a (fecha_actual menos fecha_nacimiento) los pasa a dias y los divide por 365. (Se quitan los decimales por usar doble //)
    """

    @property
    def age(self):
        if self.birth_date:
            today = datetime.date.today()
            age_alive = (today - self.birth_date).days // 365
            return age_alive
        return None

    def __str__(self):
        return f"Macota: {self.name} - {self.species}, {self.breed} - Edad: {self.age_alive}"

# Modelo de datos para la tabla de VACUNAS
class Vaccines(models.Model):
    id_pet = models.ForeignKey(Pet, on_delete=models.CASCADE) # FK de la mascota
    name_vaccine = models.CharField(max_length=100)
    date_vaccine = models.DateField(auto_now_add=True)

    def __str__(self):
         return f"Vacuna: {self.name} puesta el día {self.name_vaccine}"
    
# Modelo de datos para la tabla de CITAS MÉDICAS
class Appointment(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE) # FK del usuario
    date_appointment = models.DateField(auto_now_add=True)
    reason = models.CharField(max_length=255)
    veterinarian = models.CharField(max_length=100)

    def __str__(self):
        return f"Cita con: {self.veterinarian} el día {self.date_appointment}"