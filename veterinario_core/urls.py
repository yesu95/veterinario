from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from web import views

urlpatterns = [
    path(
        "",
        auth_views.LoginView.as_view(template_name="formulario.html"),
        name="login",
    ),
    path("admin/", admin.site.urls),
    path("mascotas/", views.view_pets, name="mascotas"),
    path("mascotas/<int:id_pet>/", views.view_detail, name="detalle"),
    path("mascotas/añadir/", views.view_create_pet, name="añadir mascota"),
    # path("mascotas/<int:id_pet>/editar/", views.view_edit_pet, name="editar"),
    # path("mascotas/<int:id_pet>/borrar/", views.view_del_pet, name="borrar"),
]