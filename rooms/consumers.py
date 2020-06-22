import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        author = data['author']
        reciepent = data['reciepent']
        message = Message.objects.create(
            room_id = self.room_name,
            author_id=author,
            reciepent_id = reciepent,
            content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_messages(content)

    def message_to_json(self, message):
        return {
            'author': message.author.id,
            'content': message.content,
            'date_created': str(message.date_created.time().strftime ("%H:%M"))

        }

    command = {

        'new_message': new_message

    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        data = json.loads(text_data)
        self.command[data['command']](self, data)

    def send_chat_messages(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
