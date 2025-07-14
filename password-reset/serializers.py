from rest_framework import serializers
from PasswordReset.models import PasswordReset
class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = ['id', 'email', 'reset_token', 'created_at', 'expires_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'email': {'required': True, 'write_only': True},
            'reset_token': {'required': True, 'write_only': True},
            'expires_at': {'required': True, 'write_only': True}
        }
        extra_kwargs = {
            'email': {'required': True, 'write_only': True},
            'reset_token': {'required': True, 'write_only': True},
            'expires_at': {'required': True, 'write_only': True}
        }