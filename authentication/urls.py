from django.urls import path

# Import all views from the single views.py file
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    currentUserView,
    AuthRootView,
    UserInfoView
)

urlpatterns = [
    # Authentication endpoints
    path('login/', LoginView.as_view(), name='auth-login'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),

    # User info endpoints
    path('me/', currentUserView.as_view(), name='current-user'),
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    path('profile/', currentUserView.as_view(), name='user-profile'),

    # Root endpoint
    path('', AuthRootView.as_view(), name='auth-root'),
]