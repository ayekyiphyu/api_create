
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from rest_framework import routers
from authentication.views import AuthRootView, LoginView, LogoutView, RegisterView
from django.http import JsonResponse
from django.urls import reverse

def api_root(response):
    return JsonResponse({
        'message': 'Welcome to the API',    
        'endpoints': {
            'admin': reverse('admin:index'),
            'api_docs': '/api/',
            'login': reverse('login'),
            'logout': reverse('logout'),
        }
    })
        
router = routers.DefaultRouter()


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include(router.urls)),

   # Auth Endpoints
   path('api/auth/register/', RegisterView.as_view(), name='register'),  # Your register view
   path('api/auth/login/', LoginView.as_view(), name='login'),  # Your login view
   path('api/auth/logout/', LogoutView.as_view(), name='logout'),  # Your logout view
   path('api/auth/', AuthRootView.as_view(), name='auth-root'),
]
