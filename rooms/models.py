from django.db import models
from users.models import CustomUser, UserRole
from django.urls import reverse


class Room(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="creator")
    partner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="partner")
    created_for = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='room_for', null=True, blank=True)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return self.creator.email + self.partner.email

    @classmethod
    def create(cls, creator, partner, created_for):
        return cls.objects.create(creator=creator, partner=partner, created_for=created_for)

    def room_detail_url(self):
        return reverse('chatroom', args=[self.pk])


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author")
    reciepent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reciepent")
    date_created = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    file = models.FileField(upload_to='chat_data/', null=True, blank=True)

    def __str__(self):
        return self.author.email +'---->'+self.reciepent.email

    def create(self, room, author, reciepent):
        self.room = room
        self.author = author
        self.reciepent = reciepent
        self.save()
        return self

    def get_time(self):
        return self.date_created.time()
