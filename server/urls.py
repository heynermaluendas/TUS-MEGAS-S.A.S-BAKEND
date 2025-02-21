"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , re_path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login',views.login),
    re_path('register',views.register),
    re_path('profile',views.profile) ,
    path('eliminar_usuario/<str:cedula>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('modificar_usuario/<str:cedula>/', views.modificar_usuario, name='modificar_usuario'),
    path('obtener_usuarios/', views.obtener_usuarios, name='obtener_usuarios'),
    path('modificar_contratante/<str:nit_o_cc>/', views.modificar_contratante, name='modificar_contratante'),
    path('contratantes/', views.obtener_contratantes, name='obtener_contratantes'),
    path('eliminar_contratante/<str:nit_o_cc>/', views.eliminar_contratante, name='eliminar_contratante'),
    path('agregar_contratante/', views.agregar_contratante, name='agregar_contratante'),
    path('mikrotik/usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('bloquear_usuario/', views.mi_vista, name='bloquear_usuario'),
    path('desbloquear_usuario/', views.mi_vistaUnblock, name='bloquear_usuario'),
    path('contratante/<str:n_cuenta>/',  views.obtener_contratante, name='obtener_contratante'), 
]
