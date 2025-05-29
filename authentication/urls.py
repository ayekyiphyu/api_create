from django.urls import path
from authentication.views import (
    LoginView, LogoutView, RegisterView, currentUserView
)
from authentication.UserInfoView import UserInfoView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Enhanced auth root view with user-specific endpoints
@api_view(['GET'])
@permission_classes([AllowAny])
def auth_root_view(request):
    """
    Authentication API root with dynamic endpoints based on user status
    """
    user = request.user

    base_endpoints = {
        "login": "/api/auth/login/",
        "register": "/api/auth/register/",
    }

    if user.is_authenticated:
        # Authenticated user endpoints
        authenticated_endpoints = {
            **base_endpoints,
            "logout": "/api/auth/logout/",
            "current_user": "/api/auth/me/",  # More RESTful
            "user_info": "/api/auth/userinfo/",
            "profile": "/api/auth/profile/",
        }

        # Add admin endpoints for superusers
        if user.is_superuser:
            authenticated_endpoints.update({
                "admin_dashboard": "/api/auth/admin/",
                "user_management": "/api/auth/users/",
                "system_info": "/api/auth/system/",
            })

        return Response({
            "message": "Authentication API",
            "user": {
                "id": user.id,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
            },
            "endpoints": authenticated_endpoints
        })
    else:
        # Anonymous user endpoints
        return Response({
            "message": "Authentication API - Please login",
            "endpoints": base_endpoints
        }, status=status.HTTP_401_UNAUTHORIZED)

# Admin-only endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_view(request):
    """Admin dashboard - superuser only"""
    if not request.user.is_superuser:
        return Response(
            {"error": "Superuser access required"},
            status=status.HTTP_403_FORBIDDEN
        )

    # # Import here to avoid circular imports
    # from django.contrib.auth.models import User

    # return Response({
    #     "message": "Admin Dashboard",
    #     "stats": {
    #         "total_users": User.objects.count(),
    #         "superusers": User.objects.filter(is_superuser=True).count(),
    #         "staff_users": User.objects.filter(is_staff=True).count(),
    #     }
    # })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def system_info_view(request):
    """System information - superuser only"""
    if not request.user.is_superuser:
        return Response(
            {"error": "Superuser access required"},
            status=status.HTTP_403_FORBIDDEN
        )

    import django
    import sys
    from django.conf import settings

    return Response({
        "django_version": django.get_version(),
        "python_version": sys.version,
        "debug_mode": settings.DEBUG,
        "database": settings.DATABASES['default']['ENGINE'],
    })

# User management for admins
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_view(request):
    """List all users - superuser only"""
    if not request.user.is_superuser:
        return Response(
            {"error": "Superuser access required"},
            status=status.HTTP_403_FORBIDDEN
        )

    from django.contrib.auth.models import User
    users = User.objects.all().values('id', 'username', 'email', 'is_superuser', 'is_staff', 'date_joined')

    return Response({
        "users": list(users),
        "total": User.objects.count()
    })

# Enhanced current user view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_enhanced(request):
    """Enhanced current user info with permissions"""
    user = request.user
    return Response({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'permissions': {
            'can_access_admin': user.is_superuser,
            'can_manage_users': user.is_superuser,
            'can_view_system_info': user.is_superuser,
        },
        'groups': [group.name for group in user.groups.all()],
    })

# URL patterns with better organization
urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='auth-login'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),

    # User info endpoints (more RESTful naming)
    path('me/', current_user_enhanced, name='current-user'),  # /api/auth/me/
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    path('profile/', currentUserView.as_view(), name='user-profile'),  # Keep your original if needed

    # Admin endpoints (protected)
    path('admin/', admin_dashboard_view, name='admin-dashboard'),
    path('users/', user_list_view, name='admin-users'),
    path('system/', system_info_view, name='system-info'),

    # Root endpoint
    path('', auth_root_view, name='auth-root'),

    # Legacy support (if needed)
    path('auth/', currentUserView.as_view(), name='current-user-legacy'),
]
