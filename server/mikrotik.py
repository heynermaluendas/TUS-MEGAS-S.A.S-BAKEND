from librouteros import connect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ssl
import json

# Configuración MikroTik
MIKROTIK_IP = '192.168.15.1'  # Cambia esto por la IP de tu MikroTik
USERNAME = 'admin'  # Cambia esto por tu usuario
PASSWORD = '3208298184O'  # Cambia esto por tu contraseña
PORT = 8728  # Puerto API de MikroTik (8728 para HTTP, 8729 para HTTPS)

# Deshabilitar verificación SSL si usas HTTPS
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def conectar_mikrotik():
    """Establece conexión con MikroTik."""
    try:
        # Conexión con MikroTik, utilizando SSL si se usa HTTPS (puerto 8729)
        api = connect(username=USERNAME, password=PASSWORD, host=MIKROTIK_IP, port=PORT, ssl_context=ssl_context)
        return api
    except Exception as e:
        return f"Error al conectar: {e}"

def obtener_usuarios_queue():
    """Obtiene la lista de usuarios en Queue Simple."""
    api = conectar_mikrotik()
    if isinstance(api, str):
        return api  # Error en la conexión

    try:
        usuarios = list(api.path("queue/simple").select("name", "max-limit",".id"))
        print("Usuarios obtenidos:", usuarios)  # Ver lo que llega
        return usuarios
    except Exception as e:
        return f"Error al obtener usuarios: {e}"

@csrf_exempt  # Exempt CSRF para permitir solicitudes POST desde fuera de Django
def block_user(request):
    """Bloquear un usuario y reducir su ancho de banda"""
    if request.method == 'POST':
        try:
            # Obtener el user_id del cuerpo de la solicitud JSON
            data = json.loads(request.body)
            user_id = data.get('user_id')
            if not user_id:
                return JsonResponse({'error': 'El parámetro user_id es necesario'}, status=400)

            api = conectar_mikrotik()
            if isinstance(api, str):
                return JsonResponse({'error': 'No se pudo conectar a MikroTik'}, status=500)

            queues = api.path('queue/simple')

            # Reducir el ancho de banda y deshabilitar la queue
            queues.update(**{'.id': user_id, 'max-limit': '1k/1k'})

            return JsonResponse({'message': 'Usuario bloqueado exitosamente con ancho de banda limitado a 1k/1k'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Error al bloquear el usuario: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt  # Exento de CSRF si lo necesitas
def unblock_user(request):
    """Desbloquear un usuario y actualizar el límite de ancho de banda"""
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            user_id = data.get('user_id')
            comment = data.get('comment')

            # Verificar si los datos son correctos
            if not user_id or not comment:
                return JsonResponse({'message': 'Error: user_id and comment are required'}, status=400)

            # Usar el comentario como el nuevo valor de 'max-limit'
            max_limit = comment

            # Llamar a la función que actualiza la cola del usuario
            success = update_queue(user_id, max_limit)

            if success:
                return JsonResponse({'message': 'Usuario desbloqueado y max-limit actualizado exitosamente'}, status=200)
            else:
                return JsonResponse({'message': 'Error al actualizar la cola del usuario'}, status=500)

        except Exception as e:
            return JsonResponse({'message': f'Error interno: {str(e)}'}, status=500)

    else:
        return JsonResponse({'message': 'Método no permitido'}, status=405)

def update_queue(user_id, max_limit):
    """Actualizar el límite de ancho de banda de la cola"""
    api = conectar_mikrotik()
    if isinstance(api, str):
        return False  # Error de conexión

    try:
        queues = api.path('queue/simple')

        # Actualizar el max-limit de la cola del usuario
        queues.update(**{'.id': user_id, 'max-limit': max_limit})

        # Si todo va bien, devolver True
        return True
    except Exception as e:
        print(f"Error al actualizar la cola: {str(e)}")
        return False
