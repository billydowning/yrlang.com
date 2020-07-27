# import code; code.interact(local=dict(globals(), **locals()))
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (FormView, TemplateView, )

from customemixing.session_and_login_mixing import UserSessionAndLoginCheckMixing
from users.models import CustomUser, Language, UserRole
import json
from .models import *
from .forms import MessageForm


class ContactPersonView(UserSessionAndLoginCheckMixing, FormView):
    form_class = MessageForm
    template_name = "create_chatroom.html"

    def form_valid(self, form):
        message = form.save(commit=False)
        if self.kwargs.get('user_role'):
            role = UserRole.objects.get(name=self.kwargs.get('user_role'))
        else:
            if self.request.user.is_language_verifier_user(self.request.session.get('user_role')):
                role = UserRole.objects.get(name=UserRole.LANGUAGE_VERIFIER)
            else:
                role = UserRole.objects.get(name=UserRole.LOCALITE)
        current_user = CustomUser.get(self.request.user.id)
        partner = CustomUser.get(self.kwargs.get('partner_id'))
        room = Room.create(current_user, partner, role)
        message.create(room, current_user, partner)
        return redirect("chatroom", room_id=room.id)

    def get(self, request, *args, **kwargs):
        current_user = CustomUser.get(request.user.id)
        partner = CustomUser.get(kwargs.get('partner_id'))
        if self.kwargs.get('user_role'):
            role = UserRole.objects.get(name=self.kwargs.get('user_role'))
        else:
            if self.request.user.is_language_verifier_user(self.request.session.get('user_role')):
                role = UserRole.objects.get(name=UserRole.LANGUAGE_VERIFIER)
            else:
                role = UserRole.objects.get(name=UserRole.LOCALITE)
        if Room.objects.filter(creator=current_user, partner=partner, created_for=role).exists():
            room = Room.objects.filter(creator=current_user, partner=partner).first()
            return redirect('chatroom', room_id=room.id)
        elif Room.objects.filter(creator=partner, partner=current_user, created_for=role).exists():
            room = Room.objects.filter(creator=partner, partner=current_user).first()
            return redirect('chatroom', room_id=room.id)
        return super(ContactPersonView, self).get(request, *args, **kwargs)

from django.utils import timezone
class ChatRoomView(UserSessionAndLoginCheckMixing, FormView):
    form_class = MessageForm
    template_name = "chatroom.html"

    def get_context_data(self, **kwargs):
        context = super(ChatRoomView, self).get_context_data(**kwargs)
        room = Room.objects.get(id=self.kwargs.get('room_id'))
        if self.request.user.id == room.creator.id:
            chatpartner = CustomUser.objects.get(id=room.partner.id)
            chat_messages = Message.objects.filter(room=room)
            Message.objects.filter(room=room).update(is_read=True)
        elif self.request.user.id == room.partner.id:
            chatpartner = CustomUser.objects.get(id=room.creator.id)
            chat_messages = Message.objects.filter(room=room)
            Message.objects.filter(room=room).update(is_read=True)
        context["room_id"] = room.id
        context["chat_messages"] = chat_messages
        context["chatpartner"] = chatpartner
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            room = Room.objects.get(id=self.kwargs.get('room_id'))
            room_chat_list = Message.objects.filter(room=room).order_by('date_created')
            chat_lst2 = [{'author': str(chat.author.id), 'date_created': str(chat.date_created.strftime ("%m/%d/%y, %H:%M")),
                          'content': chat.content, 'reciepent': str(chat.reciepent)} for chat in room_chat_list]

            json.dumps(chat_lst2)
            return JsonResponse(data={'room': chat_lst2})
        return super(ChatRoomView, self).get( request, *args, **kwargs)

    def form_valid(self, form):
        room = Room.objects.get(id=self.kwargs.get('room_id'))
        message = form.save(commit=False)
        if self.request.user.id == room.creator.id:
            message.create(room, room.creator, room.partner)
        elif self.request.user.id == room.partner.id:
            message.create(room, room.partner, room.creator)
        messages.success(self.request, 'Your message was sent successfully!')
        return redirect('chatroom', room_id=room.id)


class InboxView(UserSessionAndLoginCheckMixing, TemplateView):
    template_name = "inbox.html"

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)
        user = CustomUser.get(self.request.user.id)
        unread_messages = []
        read_messages = []
        room_list = user.creator.all() | user.partner.all()
        for room in room_list:
            if room.creator.id != user.id:
                chat_partner = room.creator
            else:
                chat_partner = room.partner
            newest_message = Message.objects.filter(room=room).reverse().first()
            if newest_message:
                if newest_message.reciepent.id == user.id:
                    if not newest_message.is_read:
                        unread_message = {'chat_partner': chat_partner,
                                          'message': newest_message}
                        unread_messages.append(unread_message)
                    else:
                        read_message = {'chat_partner': chat_partner, "message": newest_message}
                        read_messages.append(read_message)
        context["read_messages"] = read_messages
        context["unread_messages"] = unread_messages
        return context
