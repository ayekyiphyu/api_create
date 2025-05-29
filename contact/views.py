from rest_framework import generics, permissions
from contact.models import Contact
from contact.serializers import ContactSerializer

class ContactCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]  # 全ユーザーに許可

    def get_queryset(self):
        return Contact.objects.all()  # すべての問い合わせを取得（管理者用などに使うなら）

    # perform_create は不要（userを保存する必要がないため）
