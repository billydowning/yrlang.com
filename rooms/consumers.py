import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
import base64
from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from os.path import basename
from django.core.files import File
from django.conf import settings

class ChatConsumer(WebsocketConsumer):


    def file_upload(self,data):
        folder = 'chat_data/'
        author = data['author']
        reciepent = data['reciepent']
        room = int(self.room_name)
        fs = FileSystemStorage()
        file_location = fs.location +'/'+folder+data['file']['name']
        file = base64.b64decode(data['file']['data'].split(',')[-1])
        try:
            with open(file_location, "wb") as f:
                f.write(file)
                f.close()
        except Exception as e:
            print(e)
        try:
            message_obj = Message()
            message_obj.author_id = author
            message_obj.reciepent_id = reciepent
            message_obj.room_id = room
            message_obj.file.save(basename(file_location), content=File(open(file_location, 'rb')))
        except Exception as e:
            print(e)

        content = {
            'command': 'file_type_data',
            'message': self.message_with_file(message_obj)
        }
        return self.send_chat_messages(content)


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
            'date_created': str(message.date_created.strftime ("%m/%d/%y, %H:%M"))

        }

    def message_with_file(self, message):
        return {
            'author': message.author.id,
            'content': message.content,
            'date_created': str(message.date_created.strftime("%m/%d/%y, %H:%M")),
            'location': message.file.url
        }

    command = {

        'new_message': new_message,
        'file_type_data': file_upload

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


    def receive(self, text_data=None, bytes_data=None):

        if text_data:
            data = json.loads(text_data)
            if data['command'] == 'new_message':
                self.command[data['command']](self, data)
            elif data['command'] == 'file_type_data':
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
