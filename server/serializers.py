from rest_framework import serializers
from .models import CustomUser  # Usamos CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'cedula', 'first_name', 'last_name', 'email', 'password','access']
        extra_kwargs = {
            'password': {'write_only': True},  # Aseguramos que la contraseña no sea legible
            'first_name': {'required': True},  # Aseguramos que el primer nombre sea obligatorio
            'last_name': {'required': True},   # Aseguramos que el apellido sea obligatorio
        }
