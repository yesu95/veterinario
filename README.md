# Veterinario

Mi proyecto final para Python es una app desarrollada en DJANGO de un portal para una clínica veterinaria y sus clientes.

En este portal podremos acceder tanto si somos ***personal*** de la clínica con funciones como:

- Añadir, eliminar y modificar mascotas.
- Añadir vacunas y asignarlas a mascotas y borrarlas.
- Añadir y borrar citas. 

Y las funciones de los ***usuarios***:

- Registrarnos en la plataforma.
- Crear una cita para nosotros.
- Visualizar citas y nuestras mascotas con toda su información.

## Tecnologías
Python, Django, HTML + CSS, JavaScript.

## Instalación

1. Clona o descomprime el proyecto y entra en la carpeta:
```
   cd veterinario
```
2. Crea y activa el entorno virtual:
```
   python -m venv env
   env\Scripts\activate.ps1
```
3. Instala las dependencias:
```
   pip install -r requirements.txt
```
4. Base de datos:
```
   IMPORTANTE: La base de datos se encuentra en local (db.sqlite) ya que es lo que pedían en los requisitos y criterios. Igualmente Vercel usa su propia base de datos
   totalmente aparte de ésta. Es decir, las cosas que se testeen en local, como la creación de un usuario, no se va a poder conectar en el enlace de Vercel. Esto está hecho
   por si deseas instalarlo en local y comprobar que todo funcione sin la necesidad de la base de datos en Neon.
```
5. Aplica las migraciones:
```
   python manage.py migrate
```
6. Arranca el servidor:
```
   python manage.py runserver
```
7. Abre http://127.0.0.1:8000

## Usuarios de prueba local
| Usuario | Contraseña | Rol |
|---|---|---|
| carmenvet | carmenvet1234# | Veterinario (staff) |
| jose | jose1234# | Dueño |
| maria | maria1234# | Dueño |

## Usuarios de prueba en Vercel
| Usuario | Contraseña | Rol |
|---|---|---|
| carmenvet | animalia1234#| Veterinario (staff) |
| jose | jose1234# | Dueño |

## Estructura del proyecto

```
veterinario/
├── manage.py                  # Comando principal de Django
├── requirements.txt           # Dependencias
├── README.md
├── vercel.json                # Configuración del despliegue en Vercel
├── db.sqlite3                 # Base de datos local (SQLite)
├── Logging-Veterinario.log    # Registro de actividad
├── veterinario_core/          # Configuración del proyecto
│   ├── settings.py            # Ajustes (base de datos, logging...)
│   ├── urls.py                # Rutas de la aplicación
│   ├── asgi.py
│   └── wsgi.py
└── web/                       # Aplicación principal
    ├── models.py              # Modelos: Pet, Appointment, Vaccines
    ├── views.py               # Vistas (CRUD de mascotas, citas, vacunas, registro)
    ├── forms.py               # Formularios y validaciones
    ├── exceptions.py          # Excepciones personalizadas
    ├── admin.py               # Panel de administración
    ├── migrations/            # Historial de cambios de la base de datos
    ├── templates/             # Plantillas HTML
    └── static/veterinario/    # Archivos estáticos CSS, JS, IMG, etc.
        ├── css/style.css
        ├── js/main.js
        ├── img/
        └── fonts/
```

## Logs
Se guardan en `Logging-Veterinario.log`.