from rest_framework import generics, permissions
from contact.models import Contact
from contact.serializers import ContactSerializer

class ContactCreateView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        return Contact.objects.all()
