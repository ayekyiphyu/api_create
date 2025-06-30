from rest_framework import serializers
from chat.models import Chat

# Renamed the class to 'ContactSerializer' for clarity and consistency.
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        # The model was changed from 'Chat' to 'Chat' to match the import.
        model = Chat
        # It's good practice to list all fields you want to expose.
        fields = ['id', 'name', 'email', 'message', 'created_at']

        # 'updated_at' is often an internal field, so it's removed from the main fields list.
        # 'id' and 'created_at' should be read-only as they are set by the database.
        read_only_fields = ['id', 'created_at']