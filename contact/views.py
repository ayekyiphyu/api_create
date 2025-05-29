from django.shortcuts import render
from rest_framework import generics, permissions

from contact.serializers import ContactSerializer

# Create your views here.
class ContactCreateView(generics.ListCreateAPIView):
      serializer_class = ContactSerializer
      permission_classes = [permissions.IsAuthenticated]

      permission_classes = [permissions.AllowAny]

      def get_queryset(self):
        # 自分のメモだけ取得
        return ContactCreateView.objects.filter(user=self.request.user)

      def perform_create(self, serializer):
        # 作成時に自動でログインユーザーを紐付け
        serializer.save(user=self.request.user)

def get_queryset(self):
   return Concat.objects.filter(user = self.request.user)