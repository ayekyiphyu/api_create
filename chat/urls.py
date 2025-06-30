from django.urls import path
from chat.views import ChatCreateView

urlpatterns = [
    path('chat/', ChatCreateView.as_view(), name='chat-list-create'),
]