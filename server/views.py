from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model
from .models import CustomUser  # Usamos CustomUser
from django.http import JsonResponse
from server.models import CustomUser
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from server.models import CustomUser
from django.shortcuts import get_object_or_404
from .models import Contratante

@api_view(['GET'])
def obtener_usuarios(request):
    try:
        # Obtenemos todos los usuarios de la base de datos
        usuarios = CustomUser.objects.all()
        
        # Serializamos los datos
        serializer = UserSerializer(usuarios, many=True)
        
        # Retornamos la lista de usuarios
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    print("Datos recibidos:", request.data)
    # Intentamos encontrar al usuario con la cédula proporcionada
    user = get_object_or_404(CustomUser, cedula=request.data['cedula'])

    # Verificamos si la contraseña es correcta
    if not user.check_password(request.data["password"]):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

    # Creamos o recuperamos el token de autenticación
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    # Respondemos con el token y los datos del usuario
    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@csrf_exempt
def eliminar_usuario(request, cedula):
    try:
        # Buscar al usuario por su cédula
        usuario = get_object_or_404(CustomUser, cedula=cedula)
        
        # Eliminar el usuario
        usuario.delete()
        
        # Retornar una respuesta exitosa
        return JsonResponse({'message': 'Usuario eliminado exitosamente.'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt  # Si es necesario para permitir solicitudes POST sin token CSRF
def modificar_usuario(request, cedula):
    if request.method == 'POST':
        try:
            # Obtener los datos del body en formato JSON
            data = json.loads(request.body)

            # Buscar al usuario por cédula
            usuario = get_object_or_404(CustomUser, cedula=cedula)

            # Actualizar los campos del usuario
            usuario.first_name = data.get('first_name', usuario.first_name)
            usuario.last_name = data.get('last_name', usuario.last_name)
            usuario.email = data.get('email', usuario.email)
            usuario.access = data.get('access', usuario.access)
            # También puedes agregar otros campos que deseas modificar

            # Guardar los cambios
            usuario.save()

            return JsonResponse({'message': 'Usuario actualizado exitosamente.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido, usa POST.'}, status=405)

@csrf_exempt
@api_view(['POST'])
def register(request):
    # Creamos un nuevo usuario a partir de los datos proporcionados
    serializer = UserSerializer(data=request.data)
    print("Datos recibidos:", request.data)
    if serializer.is_valid():
        # Guardamos el usuario en la base de datos
        user = serializer.save()

        # Recuperamos el usuario creado y establecemos la contraseña
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Creamos un token para el nuevo usuario
        token = Token.objects.create(user=user)

        # Eliminar la contraseña del diccionario de datos antes de devolverlo
        user_data = serializer.data
        user_data.pop('password', None)  # Eliminar el campo 'password'

        return Response({'token': token.key, 'user': user_data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):

    print(request.user)
    serializer = UserSerializer(instance=request.user)
    return Response("you are login with{}".format(request.user.username),status=status.HTTP_200_OK)

def obtener_contratantes(request):
    contratantes = Contratante.objects.all()
    data = []
    for contratante in contratantes:
        data.append({
            "contratante": contratante.contratante,
            "direccion": contratante.direccion,
            "municipio": contratante.municipio,
            "telefono": contratante.telefono,
            "nit_o_cc": contratante.nit_o_cc,
            "correo": contratante.correo,
            "deuda": contratante.deuda,
            "total": contratante.total,
            "tipo_factura": contratante.tipo_factura,
            "mes_atrasado": contratante.mes_atrasado,
            "mes_actual": contratante.mes_actual,
            "precio_mes_actual": contratante.precio_mes_actual,
            "plan_contratado_mes_actual": contratante.plan_contratado_mes_actual,
            "plan_contratado_mes_atrasado": contratante.plan_contratado_mes_atrasado,
            "fecha_instalacion": contratante.fecha_instalacion,
        })
    return JsonResponse(data, safe=False)
@csrf_exempt
def obtener_contratante(request, n_cuenta):
    contratante = get_object_or_404(Contratante, mes_atrasado=n_cuenta)  # Filtra por mes_atrasado
    data = {
        "NCuenta": contratante.mes_atrasado,  # NCuenta proviene de mes_atrasado
        "contratante": contratante.contratante,
        "direccion": contratante.direccion,
        "municipio": contratante.municipio,
        "telefono": contratante.telefono,
        "nit_o_cc": contratante.nit_o_cc,
        "correo": contratante.correo,
        "deuda": contratante.deuda,
        "total": contratante.total,
        "tipo_factura": contratante.tipo_factura,
        "mes_atrasado": contratante.mes_atrasado,
        "mes_actual": contratante.mes_actual,
        "precio_mes_actual": contratante.precio_mes_actual,
        "plan_contratado_mes_actual": contratante.plan_contratado_mes_actual,
        "plan_contratado_mes_atrasado": contratante.plan_contratado_mes_atrasado,
        "fecha_instalacion": contratante.fecha_instalacion,
    }
    return JsonResponse(data)
@csrf_exempt
def modificar_contratante(request, nit_o_cc):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contratante = Contratante.objects.get(nit_o_cc=nit_o_cc)
            contratante.contratante = data.get('contratante', contratante.contratante)
            contratante.direccion = data.get('direccion', contratante.direccion)
            contratante.municipio = data.get('municipio', contratante.municipio)
            contratante.telefono = data.get('telefono', contratante.telefono)
            contratante.nit_o_cc = data.get('nit_o_cc', contratante.nit_o_cc)
            contratante.correo = data.get('correo', contratante.correo)
            contratante.deuda = data.get('deuda', contratante.deuda)
            contratante.total = data.get('total', contratante.total)
            contratante.tipo_factura = data.get('tipo_factura', contratante.tipo_factura)
            contratante.mes_atrasado = data.get('mes_atrasado', contratante.mes_atrasado)
            contratante.mes_actual = data.get('mes_actual', contratante.mes_actual)
            contratante.precio_mes_actual = data.get('precio_mes_actual', contratante.precio_mes_actual)
            contratante.plan_contratado_mes_actual = data.get('plan_contratado_mes_actual', contratante.plan_contratado_mes_actual)
            contratante.plan_contratado_mes_atrasado = data.get('plan_contratado_mes_atrasado', contratante.plan_contratado_mes_atrasado)
            contratante.fecha_instalacion = data.get('fecha_instalacion', contratante.fecha_instalacion)
            
            contratante.save()
            return JsonResponse({"message": "Contratante modificado exitosamente"})
        except Contratante.DoesNotExist:
            return JsonResponse({"error": "Contratante no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def eliminar_contratante(request, nit_o_cc):
    if request.method == 'DELETE':
        try:
            # Buscar el contratante por el NIT o cédula
            contratante = Contratante.objects.get(nit_o_cc=nit_o_cc)
            
            # Eliminar el contratante
            contratante.delete()
            
            return JsonResponse({"message": "Contratante eliminado exitosamente"})
        except Contratante.DoesNotExist:
            return JsonResponse({"error": "Contratante no encontrado"}, status=404)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def agregar_contratante(request):
    if request.method == 'POST':
        try:
            # Obtener los datos de la solicitud
            data = json.loads(request.body)
            
            # Crear un nuevo contratante con los datos recibidos
            nuevo_contratante = Contratante(
                tipo_factura=data.get('tipo_factura', 'general'),
                contratante=data.get('contratante'),
                mes_atrasado=data.get('mes_atrasado', ''),
                mes_actual=data.get('mes_actual', ''),
                precio_mes_actual=data.get('precio_mes_actual', 0),
                precio_mes_atrasado=data.get('precio_mes_atrasado', 0),
                plan_contratado_mes_atrasado=data.get('plan_contratado_mes_atrasado', ''),
                plan_contratado_mes_actual=data.get('plan_contratado_mes_actual', ''),
                deuda=data.get('deuda', 0),
                dane=data.get('dane', ''),
                fecha_instalacion=data.get('fecha_instalacion', ''),
                total=data.get('total', 0),
                nit_o_cc=data.get('nit_o_cc'),  # Este campo debe ser único
                direccion=data.get('direccion', ''),
                municipio=data.get('municipio', ''),
                telefono=data.get('telefono', ''),
                correo=data.get('correo', '')
            )
            
            # Guardar el nuevo contratante en la base de datos
            nuevo_contratante.save()
            
            return JsonResponse({"message": "Contratante agregado exitosamente"}, status=201)
        
        except Exception as e:
            return JsonResponse({"error": f"Hubo un error al agregar el contratante: {str(e)}"}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)

from django.http import JsonResponse
from .mikrotik import obtener_usuarios_queue, block_user,unblock_user
@csrf_exempt
def lista_usuarios(request):
    """Vista para obtener la lista de usuarios en el queue de MikroTik"""
    usuarios = obtener_usuarios_queue()
    return JsonResponse({'usuarios': usuarios})


@csrf_exempt  # Si necesitas la exención de CSRF también en esta vista
def mi_vista(request):
    # Llama a la función block_user desde mikrotik.py
    return block_user(request)
@csrf_exempt  # Si necesitas la exención de CSRF también en esta vista
def mi_vistaUnblock(request):
    print(request)
    # Llama a la función block_user desde mikrotik.py
    return unblock_user(request)
