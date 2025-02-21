from django.urls import re_path
from server.consumers import SessionConsumer

websocket_urlpatterns = [
    re_path(r'ws/sessions/', SessionConsumer.as_asgi()),  # Definir la ruta WebSocket
]
