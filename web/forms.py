from django import forms
from .models import Pet


class Petform(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "species", "breed", "birth_date"]

        # Para que en los formularios HTML se vean en español
        labels = {
            "name": "Nombre de la mascota",
            "species": "Especie",
            "breed": "Raza",
            "birth_date": "Fecha de nacimiento",
        }

        widgets = {
            # Renderiza el selector de fecha del navegador en formato AAAA-MM-DD
            "birth_date": forms.DateInput(
                format="%Y-%m-%d", attrs={"type": "date"}
            ),
         }