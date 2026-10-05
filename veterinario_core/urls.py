from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from web import views

urlpatterns = [
    # Login, Logout y Registro
    path(
        "",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path('registro/', views.view_register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("admin/", admin.site.urls),
    # Mascotas
    path("mascotas/", views.view_pets, name="mascotas"),
    path("mascotas/<int:id_pet>/", views.view_detail, name="detalle mascota"),
    path("mascotas/añadir/", views.view_create_pet, name="añadir mascota"),
    path("mascotas/<int:id_pet>/editar/", views.view_edit_pet, name="editar mascota"),
    path("mascotas/<int:id_pet>/borrar/", views.view_del_pet, name="borrar mascota"),
    # Citas
    path("citas/", views.view_appointments, name="citas"),
    path("citas/añadir/", views.view_create_appointment, name="añadir cita"),
    path("citas/<int:id_appointment>/borrar/", views.view_del_appointment, name="borrar cita"),
    # Vacunas  
    path("vacunas/", views.view_vaccines, name="vacunas"),
    path("vacunas/añadir/", views.view_create_vaccine, name="añadir vacuna"),
    path("vacunas/<int:id_vaccine>/borrar/", views.view_del_vaccine, name="borrar vacuna"),
]
