from rest_framework import generics, permissions
from chat.models import Chat
from chat.serializers import ChatSerializer


class ChatCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return Chat.objects.all()
