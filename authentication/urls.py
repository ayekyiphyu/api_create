from django.urls import path
from authentication.views import LoginView, LogoutView, RegisterView
from authentication.UserInfoView import UserInfoView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def auth_root_view(request):
    return Response({
        "message": "Authentication API",
        "endpoints": {
            "login": "/api/auth/login/",
            "register": "/api/auth/register/",
            "logout": "/api/auth/logout/",
            "user_info": "/api/auth/userinfo/"
        }
    })

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', auth_root_view, name='auth-root'),  # /api/auth/
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
]