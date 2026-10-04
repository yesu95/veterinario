from django import forms
from django.utils import timezone
from .models import Pet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Petform(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False, is_superuser=False),
        label="Propietario"
    )

    class Meta:
        model = Pet
        fields = ["user", "name", "species", "breed", "birth_date"]

        labels = {
            "name": "Nombre",
            "species": "Especie",
            "breed": "Raza",
            "birth_date": "Fecha de nacimiento",
        }

        widgets = {
            "birth_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "max": timezone.now().date().isoformat()
                }
            ),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get("birth_date")
        
        # Validación en el servidor
        if birth_date and birth_date > timezone.now().date():
            raise forms.ValidationError("La fecha de nacimiento no puede ser una fecha futura.")
            
        return birth_date
        

""" Form de registro de usuario """

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej. Jesús'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ej. Pérez'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'correo@ejemplo.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
