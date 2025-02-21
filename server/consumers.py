from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SessionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'some_room'  # Personaliza el nombre de la sala
        self.room_group_name = f'chat_{self.room_name}'

        # Unirse al grupo de canal
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de canal cuando la conexión se cierre
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Recibir mensajes del WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Enviar el mensaje al grupo de canal
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Enviar mensaje al WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
