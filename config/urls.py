from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse

# Views from your apps
from contact.views import ContactCreateView
from memos.views import (
    MemoListCreateView,
    MemoRetrieveUpdateDestroyView,
    MemoDeleteView,
)
from notices.views import NoticeDeleteView, NoticeEditView, NoticesCreateView
from book_calendar.views import (
    BookingListCreateView,
    BookingDetailView
)
from weather.views import WeatherCreateView

# DRF router (if you use any ViewSets)
router = DefaultRouter()
# Example: router.register(r'memos', MemoViewSet)

# Simple API root view
def root_view(request):
    return JsonResponse({
        "message": "📌 Welcome to the Dashboard API!",
        "available_endpoints": [
            "/api/auth/",
            "/api/memos/",
            "/api/notices/",
            "/api/contact/",
            "/api/calendar/",
            "/api/weather"
            "/api/weather/",
            "/api/password-reset/"
        ]
    })

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root API welcome
    path('', root_view, name='api-root'),

    # Router endpoints (if using any)
    path('api/', include(router.urls)),

    # Authentication
    path('api/auth/', include('authentication.urls')),

    # Notices
    path('api/notices/', NoticesCreateView.as_view(), name='notices-create'),

    # Memos
    path('api/memos/', MemoListCreateView.as_view(), name='memo-list-create'),
    path('api/memos/<int:pk>/', MemoRetrieveUpdateDestroyView.as_view(), name='memo-detail'),
    path('api/memos/<int:pk>/delete/', MemoDeleteView.as_view(), name='memo-delete'),

    # Contact
    path('api/contact/', ContactCreateView.as_view(), name='contact-create'),

    # Calendar
    path('api/calendar/', BookingListCreateView.as_view(), name='calendar-list-create'),
    path('api/calendar-details', BookingDetailView.as_view(), name='calendar-detail'),
    path('api/calendar/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),

    # Weather
    path('api/weather/', WeatherCreateView.as_view(), name='weather-list-create'),
<<<<<<< HEAD
]
=======

    # Password Reset - Updated to use consistent naming
    path('api/password-reset/', include('password_reset.urls')),
]
>>>>>>> origin/issue#2
