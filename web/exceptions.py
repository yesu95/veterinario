""" Excepciones personalizadas de la app """

class VetError(Exception):
    """Error de la app."""

class PetError(VetError):
    """Error relacionado con las mascotas"""

class AppointmentError(VetError):
    """Error relacionado con las citas"""

class VaccineError(VetError):
    """Error relacionado con las vacunas"""