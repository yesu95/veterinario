from django.db import models
import datetime

"""
Fechas: Auto add now crea con la fecha de ahora. Vacío preguntará la fecha obligatoriamente
"""

# Modelo de datos para la tabla de USUARIOS 
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"Usario: {self.name} - Email: {self.email}"

# Modelo de datos para la tabla de MASCOTAS 
class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # FK del usuario | Delete cascade: Si se borra Usuarios, se elimina este campo
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=80)
    breed = models.CharField(max_length=80)
    birth_date = models.DateField()  

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
        return f"Mascota: {self.name} - {self.species}, {self.breed} - Edad: {self.age}"

# Modelo de datos para la tabla de VACUNAS
class Vaccines(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE) # FK de la mascota
    name_vaccine = models.CharField(max_length=100)
    date_vaccine = models.DateField() 
    def __str__(self):
         return f"Vacuna: {self.name_vaccine} puesta el día {self.date_vaccine}"
    
# Modelo de datos para la tabla de CITAS MÉDICAS
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # FK del usuario
    date_appointment = models.DateField() 
    reason = models.CharField(max_length=255)
    veterinarian = models.CharField(max_length=100)

    def __str__(self):
        return f"Cita con: {self.veterinarian} el día {self.date_appointment}"