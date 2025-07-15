# password_reset/urls.py
from django.urls import path
from django.http import JsonResponse
from . import views

def password_reset_info(request):
    """Info view for password reset endpoints"""
    return JsonResponse({
        "message": "Password Reset API",
        "available_endpoints": {
            "request": "/api/password-reset/request/ (POST)",
            "verify": "/api/password-reset/verify/ (POST)",
            "confirm": "/api/password-reset/confirm/ (POST)"
        }
    })

urlpatterns = [
    path('', password_reset_info, name='password_reset_info'),
    path('request/', views.password_reset_request, name='password_reset_request'),
    path('confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('verify/', views.verify_reset_token, name='verify_reset_token'),
]