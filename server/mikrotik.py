# MIKROTIK_SERVERS = {
#     "1": {"ip": "186.96.97.246", "username": "admin", "password": "3208298184", "prefix": "#1"},
#     "2": {"ip": "191.97.15.98", "username": "admin", "password": "3208298184O", "prefix": "#2"},
# }
from librouteros import connect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ssl
import json

MIKROTIK_SERVERS = {
     "1": {"ip": "186.96.97.246", "username": "admin", "password": "3208298184", "prefix": "#1"},
    "2": {"ip": "191.97.15.98", "username": "admin", "password": "3208298184O", "prefix": "#2"},
}

PORT = 8728  # API de MikroTik

# Configurar SSL (solo necesario si usas HTTPS)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def conectar_mikrotik(mikrotik_config):
    """Establece conexión con un servidor MikroTik."""
    try:
        return connect(
            username=mikrotik_config["username"],
            password=mikrotik_config["password"],
            host=mikrotik_config["ip"],
            port=PORT,
            ssl_context=ssl_context
        )
    except Exception as e:
        print(f"Error al conectar a {mikrotik_config['ip']}: {e}")
        return None

def obtener_servidor(user_id):
    """Determina qué MikroTik manejará el usuario."""
    for mikrotik_id, config in MIKROTIK_SERVERS.items():
        if user_id.startswith(config["prefix"]):
            return config, user_id[len(config["prefix"]):]  # Devuelve config y user_id sin el prefijo
    return None, None

@csrf_exempt
def block_user(request):
    """Bloquea a un usuario reduciendo su ancho de banda."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'El parámetro user_id es necesario'}, status=400)

        mikrotik_config, real_user_id = obtener_servidor(user_id)
        if not mikrotik_config:
            return JsonResponse({'error': 'Servidor MikroTik no encontrado para este usuario'}, status=400)

        api = conectar_mikrotik(mikrotik_config)
        if not api:
            return JsonResponse({'error': 'No se pudo conectar a MikroTik'}, status=500)

        queues = api.path('queue/simple')
        queues.update(**{'.id': real_user_id, 'max-limit': '1k/1k'})

        return JsonResponse({'message': f'Usuario {real_user_id} bloqueado en {mikrotik_config["ip"]}'}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Error al bloquear usuario: {str(e)}'}, status=500)

@csrf_exempt
def unblock_user(request):
    """Desbloquea a un usuario y restaura su ancho de banda."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        max_limit = data.get('comment')  # Se usa el comentario como nuevo max-limit

        if not user_id or not max_limit:
            return JsonResponse({'error': 'user_id y comment son requeridos'}, status=400)

        mikrotik_config, real_user_id = obtener_servidor(user_id)
        if not mikrotik_config:
            return JsonResponse({'error': 'Servidor MikroTik no encontrado para este usuario'}, status=400)

        api = conectar_mikrotik(mikrotik_config)
        if not api:
            return JsonResponse({'error': 'No se pudo conectar a MikroTik'}, status=500)

        queues = api.path('queue/simple')
        queues.update(**{'.id': real_user_id, 'max-limit': max_limit})

        return JsonResponse({'message': f'Usuario {real_user_id} desbloqueado en {mikrotik_config["ip"]}'}, status=200)

    except Exception as e:
        return JsonResponse({'error': f'Error al desbloquear usuario: {str(e)}'}, status=500)

# def obtener_usuarios_queue():
#     """Obtiene todos los usuarios en Queue Simple de los MikroTik."""
#     usuarios_totales = []
    
#     for key, server in MIKROTIK_SERVERS.items():
#         api = conectar_mikrotik(server)
#         if not api:
#             continue  # Saltar servidores que no respondan

#         try:
#             usuarios = list(api.path("queue/simple").select("name", "max-limit", ".id"))
#             for usuario in usuarios:
#                 usuario["mikrotik_id"] = key  # Indica de qué MikroTik proviene
#             usuarios_totales.extend(usuarios)
#         except Exception as e:
#             print(f"Error al obtener usuarios de {server['ip']}: {e}")

#     return usuarios_totales

def obtener_usuarios_queue():
    all_users = []

    for server_id, details in MIKROTIK_SERVERS.items():
        try:
            # Establecer conexión con MikroTik
            api = connect(username=details["username"], password=details["password"], host=details["ip"])
            
            # Obtener la lista de usuarios del queue
            users = api(cmd="/queue/simple/print")

            # Agregar el prefijo correspondiente a cada usuario
            for user in users:
                user[".id"] = f"{details['prefix']}{user['.id']}"
                all_users.append(user)

        except Exception as e:
            print(f"Error al conectar a {details['ip']}: {e}")

    return all_users

