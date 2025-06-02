# from django.contrib import admin
# from django.urls import path, include
# from rest_framework import routers
# from django.http import JsonResponse
# from django.urls import reverse

# from contact.views import ContactCreateView
# from memos.views import MemoListCreateView, MemoRetrieveUpdateDestroyView, MemoDeleteView
# from notices.views import NoticesCreateView

# def api_root(response):
#     return JsonResponse({
#         'message': 'Welcome to the API',
#         'endpoints': {
#             'admin': reverse('admin:index'),
#             'api_docs': '/api/',
#             'login': '/api/auth/login/',
#             'logout': '/api/auth/logout/',
#             'contact': '/api/contact',
#             'notices':'/api/notices',
#             'bookings': '/api/bookings'
#         }
#     })

# router = routers.DefaultRouter()

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(router.urls)),
#     path('api/auth/', include('authentication.urls')),
#     path('api/memos/', MemoListCreateView.as_view(), name='memo-list-create'),
#     path('api/memos/<int:pk>/', MemoRetrieveUpdateDestroyView.as_view(), name='memo-detail'),
#     path('api/memos/<int:pk>/delete/', MemoDeleteView.as_view(), name='memo-delete'),
#     path('api/contact/', ContactCreateView.as_view(), name='contact-list-create'),
#     path('api/notices/', NoticesCreateView.as_view(), name='notices-list-create'),


# ]



from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
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

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),

    # DRF router URLs (for ViewSets)
    path('api/', include(router.urls)),

    # Auth endpoints
    path('api/auth/', include('authentication.urls')),
    path('api/', include('notices.urls')),

    # Memo endpoints
    path('api/memos/', MemoListCreateView.as_view(), name='memo-list-create'),
    path('api/memos/<int:pk>/', MemoRetrieveUpdateDestroyView.as_view(), name='memo-detail'),
    path('api/memos/<int:pk>/delete/', MemoDeleteView.as_view(), name='memo-delete'),

    # Contact and notices
    path('api/contact/', ContactCreateView.as_view(), name='contact-create'),
    path('api/notices/', NoticesCreateView.as_view(), name='notices-create'),



    # Booking Calendar
    path('api/bookings/', BookingListCreateView.as_view(), name= 'booking-create'),
    path('api/bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-create')
]
