import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from server.routing import websocket_urlpatterns  # Importar las rutas de WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para las rutas HTTP tradicionales
    "websocket": AuthMiddlewareStack(  # Para las rutas WebSocket
        URLRouter(
            websocket_urlpatterns  # Usamos las rutas definidas en routing.py
        )
    ),
})
