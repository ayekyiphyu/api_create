from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from authentication.views import LoginView  # Your login view

# Setup DRF routers
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api-auth/', include('rest_framework.urls')),
]