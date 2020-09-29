
from django.urls import path

from . import views


urlpatterns = [
    path('contact/<int:partner_id>', views.ContactPersonView.as_view(), name='contact'),
    path('chatroom/<int:room_id>', views.ChatRoomView.as_view(), name='chatroom'),
    path('chatroom/ajax/<int:room_id>', views.ChatRoomView.as_view(), name='chatroom_ajax'),
    path('inbox', views.InboxView.as_view(), name='inbox'),
    path('chat-log/<int:room_id>/<str:from_date>/<int:author_id>', views.ChatLogView.as_view(), name='chat_log'),
    path('chat-pdf/<int:room_id>/<str:from_date>/<int:author_id>', views.ChatLogPDFView.as_view(), name='chat_log_pdf'),
    path('chat-download/<int:room_id>/<str:from_date>/<int:author_id>', views.ChatlogDownloadAsPdfView.as_view(), name='chat_log_download'),
]