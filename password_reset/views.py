from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
import secrets
import hashlib
from django.core.mail import send_mail
from django.conf import settings

from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .models import PasswordReset

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """
    Request password reset - sends email with reset token
    """
    serializer = PasswordResetRequestSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)

            # Delete any existing password reset requests for this email
            PasswordReset.objects.filter(email=email).delete()

            # Generate secure token
            reset_token = secrets.token_urlsafe(32)
            token_hash = hashlib.sha256(reset_token.encode()).hexdigest()

            # Create new password reset record
            password_reset = PasswordReset.objects.create(
                email=email,
                reset_token=token_hash,
                expires_at=timezone.now() + timedelta(hours=1)
            )

            # Send email
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
            send_reset_email(email, reset_link)

        except User.DoesNotExist:
            # Don't reveal if email doesn't exist
            pass

        return Response({
            'message': 'If the email exists, a reset link has been sent.'
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """
    Confirm password reset with token and new password
    """
    serializer = PasswordResetConfirmSerializer(data=request.data)

    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        # Hash the token to compare with stored hash
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        try:
            # Find valid, non-expired token
            password_reset = PasswordReset.objects.get(
                reset_token=token_hash,
                expires_at__gt=timezone.now()
            )

            # Update user password
            user = User.objects.get(email=password_reset.email)
            user.password = make_password(new_password)
            user.save()

            # Delete the used token
            password_reset.delete()

            return Response({
                'message': 'Password has been reset successfully.'
            }, status=status.HTTP_200_OK)

        except PasswordReset.DoesNotExist:
            return Response({
                'error': 'Invalid or expired reset token.'
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found.'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_token(request):
    """
    Verify if reset token is valid (optional endpoint for frontend validation)
    """
    token = request.data.get('token')

    if not token:
        return Response({
            'error': 'Token is required.'
        }, status=status.HTTP_400_BAD_REQUEST)

    token_hash = hashlib.sha256(token.encode()).hexdigest()

    try:
        password_reset = PasswordReset.objects.get(
            reset_token=token_hash,
            expires_at__gt=timezone.now()
        )

        return Response({
            'message': 'Token is valid.',
            'email': password_reset.email
        }, status=status.HTTP_200_OK)

    except PasswordReset.DoesNotExist:
        return Response({
            'error': 'Invalid or expired reset token.'
        }, status=status.HTTP_400_BAD_REQUEST)

def send_reset_email(email, reset_link):
    """
    Send password reset email
    """
    subject = 'Password Reset Request'
    message = f"""
    You requested a password reset. Click the link below to reset your password:

    {reset_link}

    This link will expire in 1 hour.

    If you didn't request this, please ignore this email.
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")

# Optional: Clean up expired tokens (can be run as a management command)
def cleanup_expired_tokens():
    """
    Delete expired password reset tokens
    """
    expired_tokens = PasswordReset.objects.filter(
        expires_at__lt=timezone.now()
    )
    count = expired_tokens.count()
    expired_tokens.delete()
    return count