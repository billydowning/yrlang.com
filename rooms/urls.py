
from django.urls import path

from . import views


urlpatterns = [
    path('contact/<int:partner_id>', views.ContactPersonView.as_view(), name='contact'),
    path('chatroom/<int:room_id>', views.ChatRoomView.as_view(), name='chatroom'),
    path('chatroom/ajax/<int:room_id>', views.ChatRoomView.as_view(), name='chatroom_ajax'),
    path('inbox', views.InboxView.as_view(), name='inbox'),
]