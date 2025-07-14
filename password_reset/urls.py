from django.urls import path
from . import views

urlpatterns = [
    path('password-reset/request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/verify/', views.verify_reset_token, name='verify_reset_token'),
]