from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class CustomUser(AbstractUser):
    # El campo username se elimina al utilizar cedula como autenticador
    username = None  # Esto elimina el campo username

    cedula = models.CharField(max_length=20, unique=True, null=False, blank=False)  # La cédula es obligatoria
    first_name = models.CharField(max_length=100, null=False, blank=False)  # El nombre es obligatorio
    last_name = models.CharField(max_length=100, null=False, blank=False)  # El apellido es obligatorio
    access = models.CharField(
        max_length=50, 
        choices=[
            ('admin', 'Administrador'),
            ('editor', 'Editor'),
            ('user', 'Usuario'),
        ],
        default='user',  # Por defecto, se asigna el rol de usuario
        null=False,  # No puede ser nulo en la base de datos
        blank=False,  # No puede estar en blanco en los formularios
    )  # Campo para roles o nivel de acceso

    # Cambiar el campo de autenticación principal a 'cedula'
    USERNAME_FIELD = 'cedula'  # Usamos la cédula como el campo principal para la autenticación
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']  # Ahora necesitamos el nombre, apellido, email y contraseña

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cedula})"
 

class Contratante(models.Model):
    tipo_factura = models.CharField(max_length=100, default='general')
    contratante = models.CharField(max_length=255)
    mes_atrasado = models.CharField(
        max_length=9, 
        unique=True,   # 📌 Hace que los valores sean únicos
        null=True,     # Permite valores nulos al inicio
        blank=True     # Permite que Django no exija este campo al crear nuevos clientes
    )

    def save(self, *args, **kwargs):
        if not self.mes_atrasado:  # Si no tiene un número de cuenta, genera uno
            while True:
                numero_cuenta = str(random.randint(100000000, 999999999))  # Genera un número de 9 dígitos
                if not Contratante.objects.filter(mes_atrasado=numero_cuenta).exists():
                    self.mes_atrasado = numero_cuenta
                    break
        super().save(*args, **kwargs)
    mes_actual = models.CharField(max_length=50, null=True, blank=True)
    precio_mes_actual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_mes_atrasado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    plan_contratado_mes_atrasado = models.CharField(max_length=255, null=True, blank=True)
    plan_contratado_mes_actual = models.CharField(max_length=255, null=True, blank=True)
    deuda = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    dane = models.CharField(max_length=50, null=True, blank=True)
    fecha_instalacion = models.CharField(max_length=255, null=True, blank=True)  # Cambiado a CharField
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    nit_o_cc = models.CharField(max_length=50, unique=True)  # Campo único
    direccion = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.contratante} - {self.nit_o_cc}"
