from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.http import JsonResponse
from django.urls import reverse

from memos.views import MemoListCreateView, MemoRetrieveUpdateDestroyView, MemoDeleteView

def api_root(response):
    return JsonResponse({
        'message': 'Welcome to the API',    
        'endpoints': {
            'admin': reverse('admin:index'),
            'api_docs': '/api/',
            'login': '/api/auth/login/',
            'logout': '/api/auth/logout/',
        }
    })

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('authentication.urls')),
    path('api/memos/', MemoListCreateView.as_view(), name='memo-list-create'),
    path('api/memos/<int:pk>/', MemoRetrieveUpdateDestroyView.as_view(), name='memo-detail'),
    path('api/memos/<int:pk>/delete/', MemoDeleteView.as_view(), name='memo-delete'),
]


